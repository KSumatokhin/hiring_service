from datetime import datetime
from typing import Optional
from sqlalchemy import select
from pydantic import EmailStr
from sqlalchemy.engine import create

from app.core.config import settings
from app.core.db import get_async_session
from app.models.user import User
from app.schemas.user import AdminCreate


async def create_user(
    name: str,
    surname: Optional[str],
    tg_id: int,
    tg_username: str,
    birthday: datetime.date,
    password: str,
    email: Optional[EmailStr],
    phone: Optional[str],
):
    with get_async_session() as session:
        print("Проверка на наличие пользователей в базе данных")
        users = session.execute(select(User))
        if bool(users) is False:
            await session.execute(
                create(
                    AdminCreate(
                        name=name,
                        surname=surname,
                        tg_id=tg_id,
                        tg_username=tg_username,
                        birthday=birthday,
                        password=password,
                        email=email,
                        phone=phone,
                        role_is_admin=True,
                        is_active=True,
                    )
                )
            )


async def create_first_admin():
    if (
        settings.admin_name is not None
        and settings.admin_surname is not None
        and settings.admin_tg_id is not None
        and settings.admin_tg_username is not None
        and settings.admin_birthday is not None
        and settings.admin_password is not None
        and settings.admin_email is not None
        and settings.admin_phone is not None
    ):
        await create_user(
            name=settings.admin_name,
            surname=settings.admin_surname,
            tg_id=settings.admin_tg_id,
            tg_username=settings.admin_tg_username,
            birthday=datetime.strptime(settings.admin_birthday, "%Y-%m-%d"),
            password=settings.admin_password,
            email=settings.admin_email,
            phone=settings.admin_phone,
        )
