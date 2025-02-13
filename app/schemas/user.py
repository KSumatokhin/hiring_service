from datetime import date
import re
from typing import Optional
from pydantic import (
    BaseModel,
    EmailStr,
    Extra,
    Field,
    PositiveInt,
    field_validator,
)


class UserBase(BaseModel):
    name: str = Field(
        ...,
        min_length=2,
        max_length=100,
        description="Имя пользователя, от 2 до 100 знаков",
    )
    surname: str = Field(
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
    email: Optional[EmailStr] = Field(
        ...,
        description="Почта пользователя",
    )
    role_is_admin: bool = Field(
        default=False,
        description="Роль пользователя",
    )
    is_active: bool = Field(
        default=True,
        description="Активирован ли пользователь",
    )

    class Config:
        extra = Extra.forbid

    @field_validator("phone")
    @classmethod
    def validate_phone(cls, value: str) -> str:
        if not re.match(r"^\+\d{5,15}$", value):
            raise ValueError(
                "Номер телефона должен начинаться с '+' и содержать от 5 до 15 цифр"
            )
        return value


class AdminCreate(UserBase):
    password: str = Field(
        ...,
        min_length=8,
        max_length=50,
        description="Пароль, от 8 до 50 знаков",
    )


class UserRead(UserBase):
    pass


class UserCreate(UserBase):
    pass


class UserUpdate(UserBase):
    pass


class UserDb(UserBase):
    id: int
    surname: Optional[str]
    role_is_admin: bool
    password: Optional[str]
    is_active: bool
