"""Импорты класса Base и всех моделей для Alembic."""

from app.core.db import Base  # noqa: F401
from app.models import Keyword, Stopword, User  # noqa: F401

__ALL__ = (Base, Keyword, Stopword)

