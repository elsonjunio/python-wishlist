from sqlalchemy import select
from core.security import hash_password
from models.user import User
from core.config import settings


async def create_admin_user(session):

    admin_email = settings.ADMIN_EMAIL
    admin_username = 'admin'

    stmt = select(User).where(User.email == admin_email)
    result = await session.execute(stmt)
    admin = result.scalar_one_or_none()

    if admin:
        return admin

    admin = User(
        name=admin_username,
        email=admin_email,
        password_hash=hash_password(settings.ADMIN_PASSWORD),
        role='admin',
    )

    session.add(admin)
    await session.commit()
    await session.refresh(admin)

    return admin
