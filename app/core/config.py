from typing import Optional

from dotenv import load_dotenv
from pydantic import EmailStr
from pydantic_settings import BaseSettings

load_dotenv(".env")


class Settings(BaseSettings):
    app_title: str = "Сервис найма"
    app_description: str = "API часть для взаимодействия с Telegram-ботом"
    psg: bool
    database_psg: str
    database_sql: str
    secret: str = "secret"
    first_superuser_email: Optional[EmailStr] = None
    first_superuser_password: Optional[str] = None

    class Config:
        env_file = ".env"
        extra = "ignore"


settings = Settings()


def get_db_url():
    if os.getenv("PSG", "False").lower() == "true":
        return os.environ["DATABASE_PSG"]
    return os.environ["DATABASE_SQL"]


def get_auth_data():
    return {
        "secret_key": settings.SECRET_KEY,
        "algorithm": settings.ALGORITHM,
    }

