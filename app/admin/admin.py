from sqladmin import ModelView

from app.models import Keyword, Stopword, User


class UserAdmin(ModelView, model=User):
    column_list = [User.name, User.surname, User.tg_username]
    name = "Пользователь"
    name_plural = "Пользователи"
    icon = "fa-solid fa-user"
    category = "accounts"

    async def on_model_change(self, data, model, is_created, request) -> None:
        if is_created:
            password = data["password"]
            data["password"] = get_password_hash(password=password)


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
