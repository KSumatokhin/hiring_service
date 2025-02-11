import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr

from fastapi_users import schemas


class UserRead(schemas.BaseUser[int]):
    pass


class UserCreate(BaseModel):
    username: str
    hash_password: str
    is_superuser: bool
    is_active: bool
    # username: str
    # surname: Optional[str]
    # tg_id: str
    # tg_username: str
    # birthday: Optional[datetime.date]
    # phone: Optional[str]


class UserUpdate(schemas.BaseUserUpdate):
    pass
