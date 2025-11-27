from typing import Optional
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: Optional[str] = None
    JWT_SECRET: Optional[str] = None
    JWT_ALGORITHM: str = 'HS256'
    ENV: str = 'dev'

    ADMIN_EMAIL: str = 'admin@local.com'
    ADMIN_PASSWORD: str = 'admin123'

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'


settings = Settings()
