from sqladmin import Admin, ModelView

# from app.core.db import engine
from app.models import User
# from app.main import app


class UserAdmin(ModelView, model=User):
    column_list = [User.id, User.username]
    column_searchable_list = [User.username]


# admin = Admin(app, engine)
# admin.add_view(UserAdmin)