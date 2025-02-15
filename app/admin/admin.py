import contextlib

from sqladmin import ModelView

from app.models import Keyword, Stopword, User
from app.crud.user_01 import UserManager, get_user_db
from app.core.db import get_async_session
from app.schemas.user_01 import UserCreate


class UserAdmin(ModelView, model=User):
    column_list = [User.first_name, User.last_name, User.tg_username]
    name = "Пользователь"
    name_plural = "Пользователи"
    icon = "fa-solid fa-user"
    category = "accounts"
    column_labels = {"hashed_password": "password"}
    form_create_rules = [
        "first_name",
        "last_name",
        "tg_id",
        "tg_username",
        "birthday",
        "phone",
        "email",
        "hashed_password",
    ]

    @contextlib.asynccontextmanager
    async def get_user_manager(self):
        async for session in get_async_session():
            async for user_db in get_user_db(session):
                yield UserManager(user_db)

    async def on_model_change(self, data, model, is_created, request) -> None:
        if is_created:
            async with self.get_user_manager() as user_manager:
                data['password'] = data['hashed_password']
                data.pop('hashed_password')
                await user_manager.create(UserCreate(**data))


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
