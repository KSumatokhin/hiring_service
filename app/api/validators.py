from http import HTTPStatus

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession


async def check_word_duplicate(
    session: AsyncSession, word: str, crud_model
):
    """Общая проверка на дубликаты"""
    word_id = await crud_model.get_id_by_word(word, session)
    return word_id


async def check_word_exists(
    session: AsyncSession,
    word: str,
    crud_model,
    model_name: str
):
    """Общая проверка существования слова (ключевого или стоп-слова)"""
    word_id = await crud_model.get_id_by_word(word, session)
    if word_id is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=f'{model_name} не найдено!'
        )
    return await crud_model.get(word_id, session)
