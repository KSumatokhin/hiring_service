# from datetime import datetime

# from fastapi_users.db import SQLAlchemyBaseUserTable
# from sqlalchemy import Column, String, Date
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Boolean, Integer, String

from app.core.db import Base


# class User(SQLAlchemyBaseUserTable[int], Base):
#     username = Column(String(20), nullable=False)
#     surname = Column(String(50), nullable=True)
#     tg_id = Column(String(1024), unique=True, nullable=False)
#     tg_username = Column(String(50), unique=True, nullable=False)
#     birthday = Column(Date, nullable=False)
#     phone = Column(String(15), nullable=False)

    # name: Mapped[str] = mapped_column(String(20), nullable=False)
    # surname: Mapped[str] = mapped_column(String(50), nullable=False)
    # tg_id: Mapped[str] = mapped_column(String(1024), nullable=False)
    # tg_username: Mapped[str] = mapped_column(String(50), nullable=False)
    # birthday: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    # phone: Mapped[str] = mapped_column(String(15), nullable=False)

class User(Base):

    id: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False)
    username: Mapped[str] = mapped_column(String(length=255), nullable=False)
    hash_password: Mapped[str] = mapped_column(String(length=255), nullable=False)
    is_superuser: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    def __str__(self):
        return self.username