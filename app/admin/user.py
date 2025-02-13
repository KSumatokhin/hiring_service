from sqladmin import ModelView

from app.auth import get_password_hash
from app.exceptions import IncorrectEmailOrPasswordException
from app.models import User


class UserAdmin(ModelView, model=User):
    column_list = [User.id, User.name, User.surname, User.tg_username]
    form_create_rules = [
        'name',
        'surname',
        'tg_id',
        'tg_username',
        'birthday',
        'role_is_admin',
        'password',
        'email',
        'phone',
    ]
    form_edit_rules = [
        'name',
        'surname',
        'phone',
        'email',
        'is_active',
    ]

    async def on_model_change(self, data, model, is_created, request) -> None:
        if is_created:
            admin = data.get('role_is_admin')
            password = data.get('password', None)
            if admin and password != '':
                data['password'] = get_password_hash(password=password)
            elif admin and password == '':
                raise IncorrectEmailOrPasswordException
            else:
                data['password'] = ''
