from sqlalchemy import Column, String, BigInteger, DateTime, Enum
import enum

from app.core.db import Base


class Role(str, enum.Enum):
    ADMIN = "admin"
    USER = "user"


class User(Base):
    name = Column(String(20), nullable=False)
    surname = Column(String(50), nullable=True)
    tg_id = Column(BigInteger, unique=True, nullable=False)
    tg_username = Column(String(50), unique=True, nullable=False)
    birthday = Column(DateTime, nullable=False)
    role = Column(Enum(Role), default=Role.USER, nullable=False)
    hashed_password = Column(String)
    email = Column(String(50), nullable=False)  # Валидация email? EmailStr
    phone = Column(String(50), nullable=False)  # Валидация phone?
