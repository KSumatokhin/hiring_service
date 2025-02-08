from fastapi import FastAPI
from sqladmin import Admin, ModelView

from app.core.config import settings
from app.core.db import engine
from app.models import User


app = FastAPI(title=settings.app_title, description=settings.app_description)
admin = Admin(app, engine)


class UserAdmin(ModelView, model=User):
    column_list = [User.id, User.name]
    column_searchable_list = [User.name, User.surname]


admin.add_view(UserAdmin)

# uvicorn app.main:app --reload