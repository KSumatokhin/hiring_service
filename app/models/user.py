from sqlalchemy import (
    Boolean,
    CheckConstraint,
    Column,
    Date,
    String,
    BigInteger,
)

from app.core.db import Base


class User(Base):
    first_name = Column(String(20), nullable=False)
    last_name = Column(String(50), nullable=True)
    tg_id = Column(BigInteger, unique=True, nullable=False)
    tg_username = Column(String(50), unique=True, nullable=False)
    birthday = Column(Date, nullable=False)
    phone = Column(String(50), nullable=True)
    # role_is_admin = Column(Boolean, default=False, nullable=False)
    # password = Column(String, nullable=True)
    # email = Column(String(50), nullable=True)
    # is_active = Column(Boolean, default=True, nullable=False)

    __table_args__ = (
        CheckConstraint(
            sqltext="tg_id > 0",
            name="Positive tg_id",
        ),
    )

    def __repr__(self) -> str:
        return f"{type(self).__name__}" f"{self.name=}" f"{self.tg_username}"
