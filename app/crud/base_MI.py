from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


class CRUDBase:

    def __init__(self, model):
        self.model = model

    async def get(
        self,
        obj_id: int,
        session: AsyncSession,
    ):
        """Получение одного объекта по id."""
        db_obj = await session.execute(
            select(self.model).where(self.model.id == obj_id)
        )
        return db_obj.scalars().first()

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

    async def create(
        self, obj_in, session: AsyncSession
    ):
        """Создание объекта."""
        obj_in_data = obj_in.dict()
        db_obj = self.model(**obj_in_data)
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj

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

    async def remove(
        self,
        db_obj,
        session: AsyncSession,
    ):
        """Удаление объекта."""
        await session.delete(db_obj)
        await session.flush()
        await session.commit()
        return db_obj
