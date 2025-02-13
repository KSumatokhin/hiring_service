from typing import Optional

from fastapi.encoders import jsonable_encoder
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import User


class CRUDBase:

    def __init__(self, model):
        self.model = model

    async def get(
            self,
            obj_id: int,
            session: AsyncSession,
    ):
        db_obj = await session.execute(
            select(self.model).where(
                self.model.id == obj_id
            )
        )
        return db_obj.scalars().first()

    async def find_one_or_none(
            self,
            session: AsyncSession,
            **filter_by,
    ):
        db_obj = await session.execute(
            select(self.model).filter_by(**filter_by)
        )
        return db_obj.scalar_one_or_none()

    async def get_multi(
            self,
            session: AsyncSession
    ):
        db_objs = await session.execute(select(self.model))
        return db_objs.scalars().all()

    async def create(
            self,
            obj_in,
            session: AsyncSession,
            user: Optional[User] = None
    ):
        obj_in_data = obj_in.dict()
        if user is not None:
            obj_in_data['user_id'] = user.id
        db_obj = self.model(**obj_in_data)
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj

    async def update(
            self,
            db_obj,
            obj_in,
            session: AsyncSession,
    ):
        obj_data = jsonable_encoder(db_obj)
        update_data = obj_in.dict(exclude_unset=True)

        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj

    async def remove(
            self,
            db_obj,
            session: AsyncSession,
    ):
        await session.delete(db_obj)
        await session.commit()
        return db_obj

    async def get_id_by_word(
        self,
        word: str,
        session: AsyncSession,
    ):
        """Получение id одного объекта по слову."""
        db_obj_id = await session.execute(
            select(self.model.id).where(self.model.word == word)
        )
        return db_obj_id.scalars().first() or None

    async def get_all_words(self, session: AsyncSession):
        """Получение всех объектов."""
        db_objs_word = await session.execute(select(self.model.word))
        return db_objs_word.scalars().all()

    async def create_multi(
        self, objects_in: list, session: AsyncSession
    ):
        """Создание объектов."""
        db_obj_list = []
        for obj_in in objects_in:
            obj_in_data = obj_in.dict()
            db_obj = self.model(**obj_in_data)
            db_obj_list.append(db_obj)
        session.add_all(db_obj_list)
        await session.commit()

        for obj in db_obj_list:
            await session.refresh(obj)
        return db_obj_list
