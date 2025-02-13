from sqlalchemy import Column, String
from app.core.db import Base

from app.core.db import MAX_LENGHT


class Stopword(Base):
    word = Column(String(MAX_LENGHT), unique=True, nullable=False)

    def __repr__(self):
        return f'{self.word}'
