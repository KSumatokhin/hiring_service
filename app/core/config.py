from typing import Optional

from pydantic import EmailStr, Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class ConfigBase(BaseSettings):
    """Базовые настройки."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        env_prefix="",
    )


class ConfigApp(ConfigBase):
    """Настройки приложения."""

    model_config = SettingsConfigDict(env_prefix="APP_")
    title: str = Field(default="Word analitic")
    description: str = Field(default="Анализ слов")
    secret: SecretStr = Field(default="SECRET")
    algorithm: str = Field(default="HS256")
    debug: bool = Field(default=True)


class ConfigDB(ConfigBase):
    """Настройки базы данных."""

    model_config = SettingsConfigDict(env_prefix="DB_")
    name: str = Field(default="recruit")
    user: str = Field(default="user")
    password: str = Field(default="password")
    host: str = Field(default="localhost")
    port: str = Field(default="5432")


class ConfigAdmin(ConfigBase):
    """Настройки для первого админа."""

    model_config = SettingsConfigDict(env_prefix="ADMIN_")
    name: str = Field(default="Admin")
    surname: Optional[str] = Field(default="Admin")
    tg_id: int = Field(default=123456789)
    tg_username: str = Field(default="@admin")
    birthday: str = Field(default="2000-01-01")
    password: Optional[SecretStr] = Field(default=None)
    email: Optional[EmailStr] = Field(default=None)
    phone: Optional[str] = Field(default="+70123456789")


class Config(ConfigBase):
    """Все настройки приложения."""

    app: ConfigApp = Field(default_factory=ConfigApp)
    db: ConfigDB = Field(default_factory=ConfigDB)
    admin: ConfigAdmin = Field(default_factory=ConfigAdmin)

    @classmethod
    def load(cls) -> "Config":
        return cls()


config = Config()


def get_db_url():
    if config.app.debug:
        return f"sqlite+aiosqlite:///./{config.db.name}.db"
    return (
        f"postgresql+asyncpg://{config.db.user}"
        f":{config.db.password}@{config.db.host}:"
        f"{config.db.port}/{config.db.name}"
    )
