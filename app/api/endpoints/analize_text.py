from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.crud import key_word_crud, stop_word_crud
from app.services.morph import process_text_pipeline
from app.schemas.analise import Words


router = APIRouter()


@router.post(
    '/',
    response_model=Words
)
async def analyze_text(
    text: str,
    session: AsyncSession = Depends(get_async_session),
):
    """Анализ текста."""
    if not text.strip():
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Текст для анализа не может быть пустым.'
        )
    tokens = process_text_pipeline(text)
    data = {'key_words': [], 'stop_words': []}
    key_words_set = set(await key_word_crud.get_all_words(session))
    stop_words_set = set(await stop_word_crud.get_all_words(session))
    data['key_words'] = [word for word in tokens if word in key_words_set]
    data['stop_words'] = [word for word in tokens if word in stop_words_set]
    return data
