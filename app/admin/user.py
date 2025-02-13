from sqladmin import ModelView

# from app.core.db import engine
from app.models import User

# from app.main import app


class UserAdmin(ModelView, model=User):
    column_list = [User.id, User.name]
    form_create_rules = [
        "name",
        "surname",
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

