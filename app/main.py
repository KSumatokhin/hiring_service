from datetime import datetime
from fastapi import FastAPI

from passlib.context import CryptContext

# from sqladmin import Admin, ModelView
from sqladmin import Admin
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

# from app.api.routers import main_router

# from app.auth import get_password_hash
from app.core.config import settings
from app.core.db import engine, AsyncSessionLocal

from app.admin import UserAdmin
from app.models import User

from app.admin.auth import authentication_backend


app = FastAPI(
    title=settings.app_title,
    description=settings.app_description,
)

# app.include_router(main_router)


admin = Admin(app, engine, authentication_backend=authentication_backend)
admin.add_view(UserAdmin)


@app.on_event("startup")
async def startup():
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    hashed_password = pwd_context.hash(settings.admin_password)
    async with AsyncSessionLocal() as session:
        user = await session.execute(select(User))
        if user.first() is None:
            admin_user = dict(
                name=settings.admin_name,
                surname=settings.admin_surname,
                tg_id=int(settings.admin_tg_id),
                tg_username=settings.admin_tg_username,
                birthday=datetime.strptime(
                    settings.admin_birthday,
                    "%Y-%m-%d",
                ).date(),
                password=hashed_password,
                email=settings.admin_email,
                phone=settings.admin_phone,
                role_is_admin=True,
            )
            db_user = User(**admin_user)
            session.add(db_user)
            await session.commit()
            await session.refresh(db_user)
            print("Создан первый пользователь")


# uvicorn app.main:app --reload
