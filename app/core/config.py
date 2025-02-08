from typing import Optional

from pydantic import EmailStr
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_title: str = 'Сервис найма'
    app_description: str = 'API часть для взаимодействия с Telegram-ботом'
    psg: bool
    database_psg: str
    database_sql: str
    secret: str = 'secret'
    first_superuser_email: Optional[EmailStr] = None
    first_superuser_password: Optional[str] = None

    class Config:
        env_file = '.env'
        extra = 'ignore'


settings = Settings()
