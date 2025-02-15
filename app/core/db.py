import os
import contextlib

from dotenv import load_dotenv
from sqlalchemy import Column, Integer
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, declared_attr, sessionmaker
# from async_generator import asynccontextmanager

load_dotenv(".env")

database_url = (
    os.environ["DATABASE_SQL"] if os.environ["DEBUG"] else os.environ["DATABASE_PSG"]
)

MAX_LENGHT = 50


class PreBase:

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    id = Column(Integer, primary_key=True)


Base = declarative_base(cls=PreBase)

engine = create_async_engine(database_url)

AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession)


async def get_async_session():
    async with AsyncSessionLocal() as async_session:
        yield async_session


@contextlib.asynccontextmanager
async def async_session_manager():
    async with AsyncSessionLocal() as async_session:
        yield async_session
