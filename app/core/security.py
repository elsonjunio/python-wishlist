from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
import jwt
from core.config import settings

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)


def create_access_token(data: dict, expires: int = 60 * 24):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=expires)
    to_encode.update({'exp': expire})

    return jwt.encode(
        to_encode,
        settings.JWT_SECRET,
        algorithm=settings.JWT_ALGORITHM,
    )
