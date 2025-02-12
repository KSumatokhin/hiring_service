from fastapi import FastAPI
from sqladmin import Admin, ModelView

from app.api.routers import main_router
from app.auth import get_password_hash
from app.core.config import settings
from app.core.db import engine
from app.admin import UserAdmin
from app.models import User
from app.admin.auth import authentication_backend

from app.core.init_db import create_first_admin

app = FastAPI(title=settings.app_title, description=settings.app_description)

app.include_router(main_router)


class UserAdmin(ModelView, model=User):
    column_list = [User.id, User.first_name]
    form_create_rules = [
        "first_name",
        "last_name",
        "phone_number",
        "email",
        "password",
    ]
    form_edit_rules = [
        "first_name",
        "last_name",
        "phone_number",
        "email",
    ]

    async def on_model_change(self, data, model, is_created, request) -> None:
        if is_created:
            password = data["password"]
            # Hash the password before saving into DB !
            data["password"] = get_password_hash(password=password)


admin = Admin(app, engine, authentication_backend=authentication_backend)
admin.add_view(UserAdmin)


@app.on_event("startup")
async def startup():
    await create_first_admin()


# uvicorn app.main:app --reload
