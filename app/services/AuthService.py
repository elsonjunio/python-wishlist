from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException, status

from models.user import User
from core.security import hash_password, verify_password, create_access_token
from schemas.auth import UserCreate, UserLogin


class AuthService:
    @staticmethod
    async def register(db: AsyncSession, payload: UserCreate):
        result = await db.execute(
            select(User).where(User.email == payload.email)
        )
        exists = result.scalar_one_or_none()

        if exists:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='Email already registered',
            )

        user = User(
            name=payload.name,
            email=payload.email,
            password_hash=hash_password(payload.password),
        )

        db.add(user)
        await db.commit()
        await db.refresh(user)

        return user

    @staticmethod
    async def login(db: AsyncSession, payload: UserLogin):
        result = await db.execute(
            select(User).where(User.email == payload.email)
        )
        user = result.scalar_one_or_none()

        if not user or not verify_password(
            payload.password, user.password_hash
        ):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Invalid credentials',
            )

        token = create_access_token(
            {
                'sub': str(user.id),
                'email': str(user.email),
                'role': str(user.role),
            }
        )
        return token
