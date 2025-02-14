from typing import Optional
from datetime import date, datetime
import contextlib

from fastapi_users.exceptions import UserAlreadyExists
from pydantic import EmailStr

from app.core.config import config
from app.core.db import get_async_session
from app.core.user import get_user_db, get_user_manager
from app.schemas.user import UserCreate


get_async_session_context = contextlib.asynccontextmanager(get_async_session)
get_user_db_context = contextlib.asynccontextmanager(get_user_db)
get_user_manager_context = contextlib.asynccontextmanager(get_user_manager)


async def create_user(
    name: str,
    surname: Optional[str],
    tg_id: int,
    tg_username: str,
    birthday: date,
    password: str,
    email: Optional[EmailStr] = None,
    phone: Optional[str] = None,
):
    try:
        async with get_async_session_context() as session:
            async with get_user_db_context(session) as user_db:
                async with get_user_manager_context(user_db) as user_manager:
                    await user_manager.create(
                        UserCreate(
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
    except UserAlreadyExists:
        pass


async def create_first_superuser():
    if (
        config.admin.name is not None
        and config.admin.tg_id is not None
        and config.admin.tg_username is not None
        and config.admin.birthday is not None
        and config.admin.password is not None
    ):
        await create_user(
            name=config.admin.name,
            surname=config.admin.surname,
            tg_id=int(config.admin.tg_id),
            tg_username=config.admin.tg_username,
            birthday=datetime.strptime(
                config.admin.birthday,
                "%Y-%m-%d",
            ).date(),
            email=config.admin.email,
            password=config.admin.password.get_secret_value(),
            phone=config.admin.phone,
        )
