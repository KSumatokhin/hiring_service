import os
from datetime import datetime
from typing import Optional

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv(".env")


class Settings(BaseSettings):
    app_title: str = "Сервис найма"
    app_description: str = "API часть для взаимодействия с Telegram-ботом"
    database_psg: str
    database_sql: str
    secret: str = "secret"
    algorithm: str = "HS256"

    admin_name: str = None
    admin_surname: Optional[str] = None
    admin_tg_id: int = None
    admin_tg_username: str = None
    admin_birthday: datetime.date = None
    admin_role: Optional[bool] = None
    admin_password: str = None
    admin_email: Optional[str] = None
    admin_phone: Optional[str] = None

    class Config:
        env_file = ".env"
        extra = "ignore"


settings = Settings()


def get_db_url():
    if os.getenv("DEBUG") == 1:
        return os.environ["DATABASE_SQL"]
    return os.environ["DATABASE_PSG"]


def get_auth_data():
    return {
        "secret_key": settings.secret,
        "algorithm": settings.algorithm,
    }
