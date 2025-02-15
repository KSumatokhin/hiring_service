from datetime import datetime
from typing import Optional

from passlib.context import CryptContext
from pydantic import EmailStr
from sqlalchemy import select

from app.core.config import settings
from app.core.db import AsyncSessionLocal
from app.models import User


async def create_user(
    first_name: str,
    last_name: Optional[str],
    tg_id: int,
    tg_username: str,
    birthday: datetime,
    password: str,
    email: Optional[EmailStr],
    phone: Optional[str],
):

    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    hashed_password = pwd_context.hash(password)

    async with AsyncSessionLocal() as session:
        users = await session.execute(select(User))
        if users.first() is None:
            admin_user = dict(
                first_name=first_name,
                last_name=last_name,
                tg_id=tg_id,
                tg_username=tg_username,
                birthday=birthday,
                hashed_password=hashed_password,
                email=email,
                phone=phone,
                is_superuser=True,
                is_active=True,
            )
            db_user = User(**admin_user)
            session.add(db_user)
            await session.commit()
            await session.refresh(db_user)
            print("Создан первый администратор!")


async def create_first_admin():
    if (
        settings.admin_name is not None and
        settings.admin_surname is not None and
        settings.admin_tg_id is not None and
        settings.admin_tg_username is not None and
        settings.admin_birthday is not None and
        settings.admin_password is not None and
        settings.admin_email is not None and
        settings.admin_phone is not None
    ):
        await create_user(
            first_name=settings.admin_name,
            last_name=settings.admin_surname,
            tg_id=settings.admin_tg_id,
            tg_username=settings.admin_tg_username,
            birthday=datetime.strptime(settings.admin_birthday, "%Y-%m-%d"),
            password=settings.admin_password,
            email=settings.admin_email,
            phone=settings.admin_phone,
        )


# Можно скопировать из Яндекс Практикума, теперь добавил fastapi-users!