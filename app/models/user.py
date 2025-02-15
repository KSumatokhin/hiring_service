# app/models/user.py
from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable
from sqlalchemy import BigInteger, Column, Date, String

from app.core.db import Base


class User(SQLAlchemyBaseUserTable[int], Base):
    first_name = Column(String(20), nullable=False)
    last_name = Column(String(50), nullable=True)
    tg_id = Column(BigInteger, unique=True, nullable=False)
    tg_username = Column(String(50), unique=True, nullable=False)
    birthday = Column(Date, nullable=False)
    phone = Column(String(50), nullable=True)