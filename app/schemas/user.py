from typing import Optional
from datetime import date

from fastapi_users import schemas


class UserRead(schemas.BaseUser[int]):
    first_name: str
    last_name: Optional[str] = None
    tg_id: int
    tg_username: str
    birthday: date
    phone: Optional[str] = None


class UserCreate(schemas.BaseUserCreate):
    first_name: str
    last_name: Optional[str] = None
    tg_id: int
    tg_username: str
    birthday: date
    phone: Optional[str] = None


class UserUpdate(schemas.BaseUserUpdate):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    tg_id: Optional[int] = None
    tg_username: Optional[str] = None