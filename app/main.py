from fastapi import FastAPI


# from sqladmin import Admin, ModelView
from sqladmin import Admin

from app.api.routers import main_router

# from app.auth import get_password_hash
from app.admin.auth import AdminAuth
from app.core.config import settings
from app.core.db import engine
from app.core.init_db import create_first_admin

from app.admin import UserAdmin, KeywordAdmin, StopwordAdmin

# from app.admin.auth import authentication_backend


app = FastAPI(
    title=settings.app_title,
    description=settings.app_description,
)

app.include_router(main_router)


admin = Admin(app, engine, authentication_backend=AdminAuth())
admin.add_view(UserAdmin)
admin.add_view(KeywordAdmin)
admin.add_view(StopwordAdmin)


@app.on_event("startup")
async def startup():
    await create_first_admin()


# uvicorn app.main:app --reload
