from datetime import date
import re
from typing import Optional

from fastapi_users.schemas import BaseUserCreate
from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    PositiveInt,
    field_validator,
)


class UserBase(BaseModel):
    model_config = ConfigDict(extra="forbid", from_attributes=True)
    name: str = Field(
        ...,
        min_length=2,
        max_length=100,
        description="Имя пользователя, от 2 до 100 знаков",
    )
    surname: Optional[str] = Field(
        ...,
        min_length=2,
        max_length=100,
        description="Фамилия пользователя, от 2 до 100",
    )
    tg_id: PositiveInt = Field(
        ...,
        description="ID в Телеграме",
    )
    tg_username: str = Field(
        ...,
        max_length=2048,
        description="Имя в Телеграме, до 2048 знаков",
    )
    birthday: date = Field(
        ...,
        description="Дата рождения",
    )
    phone: Optional[str] = Field(
        ...,
        description="Номер телефона, начинает со знака '+'",
    )
    role_is_admin: bool = Field(
        default=False,
        description="Роль пользователя",
    )
    is_active: Optional[bool] = Field(
        default=True, description="Состояние пользователя"
    )

    @field_validator("phone")
    @classmethod
    def validate_phone(cls, value: str) -> str:
        if not re.match(r"^\+\d{5,15}$", value):
            raise ValueError(
                "Номер телефона должен начинаться с '+' и содержать от 5 до 15 цифр"
            )
        return value


class UserCreate(BaseUserCreate, UserBase):
    pass


class UserRead(UserBase):
    pass


class UserUpdate(UserBase):
    pass


class UserDb(UserCreate):
    id: int
