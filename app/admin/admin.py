from sqladmin import ModelView

from app.auth import get_password_hash
from app.exceptions import IncorrectEmailOrPasswordException
from app.models import Keyword, Stopword, User


class UserAdmin(ModelView, model=User):
    name = "Пользователь"
    name_plural = "Пользователи"
    icon = "fa-solid fa-user"
    category = "accounts"
    column_list = [User.name, User.surname, User.tg_username]
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


class KeywordAdmin(ModelView, model=Keyword):
    column_list = [Keyword.id, Keyword.word]
    name = "Ключевое слово"
    name_plural = "Ключевые слова"
    icon = "fa-solid fa-file-text"
    category = "keywords"
    column_searchable_list = [Keyword.word]
    column_sortable_list = [Keyword.word]


class StopwordAdmin(ModelView, model=Stopword):
    column_list = [Stopword.id, Stopword.word]
    name = "Стоп-слово"
    name_plural = "Стоп-слова"
    icon = "fa-solid fa-file-text"
    category = "stopwords"
    column_searchable_list = [Stopword.word]
    column_sortable_list = [Stopword.word]
