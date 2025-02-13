from http import HTTPStatus

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import (
    check_word_duplicate,
    check_word_exists
)
from app.core.db import get_async_session
from app.core.user import current_superuser
from app.crud import stop_word_crud
from app.models.stop_word import Stopword
from app.schemas.stop_word import (
    StopwordCreate, StopWordsCreateList, StopwordDB
)
from app.services.morph import lemmatize_word


router = APIRouter()


@router.get(
    '/',
    response_model=list[str],
)
async def get_all_stop_words(
    session: AsyncSession = Depends(get_async_session),
):
    """Список всех стоп-слов."""
    return await stop_word_crud.get_all_words(session)


@router.post(
    '/',
    response_model=StopwordDB,
    dependencies=[Depends(current_superuser)],
)
async def create_new_stop_word(
    stop_word: StopwordCreate,
    session: AsyncSession = Depends(get_async_session),
):
    """Создание стоп-слова. Только для суперюзеров."""
    stop_word.word = lemmatize_word(stop_word.word.lower())
    stop_word_id = await check_word_duplicate(
        session, stop_word.word, stop_word_crud
    )
    if stop_word_id:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Такое стоп-слово уже существует!'
        )
    return await stop_word_crud.create(stop_word, session)


@router.post(
        '/batch', response_model=list[StopwordDB],
        dependencies=[Depends(current_superuser)]
    )
async def create_stop_words_batch(
    words_in: StopWordsCreateList,
    session: AsyncSession = Depends(get_async_session),
):
    """Создание нескольких стоп-слов за один раз."""
    created_objs = []
    to_create = []
    exists_obj = []
    for word in words_in.words:
        lemma = lemmatize_word(word.lower())
        stop_word_id = await check_word_duplicate(
            session, lemma, stop_word_crud
        )
        if stop_word_id:
            exists_obj.append(
                Stopword(id=stop_word_id, word=f'{lemma} уже существует')
            )
        else:
            to_create.append(StopwordCreate(word=lemma))
    created_objs = await stop_word_crud.create_multi(to_create, session)
    created_objs.extend(exists_obj)
    return created_objs


@router.post(
        '/upload-file', response_model=list[StopwordDB],
        dependencies=[Depends(current_superuser)]
    )
async def upload_stop_words_file(
    file: UploadFile = File(...),
    session: AsyncSession = Depends(get_async_session)
):
    """Загрузка списка стоп-слов из файла."""
    lines = (await file.read()).decode("utf-8").splitlines()
    created_objs = []
    to_create = []
    exists_obj = []
    for line in lines:
        cleaned = line.strip()
        if not cleaned:
            continue
        lemma = lemmatize_word(cleaned.lower())
        stop_word_id = await check_word_duplicate(
            session, lemma, stop_word_crud
        )
        if stop_word_id:
            exists_obj.append(
                Stopword(id=stop_word_id, word=f'{lemma} уже существует')
            )
        else:
            to_create.append(StopwordCreate(word=lemma))
    created_objs = await stop_word_crud.create_multi(to_create, session)
    created_objs.extend(exists_obj)
    return created_objs


@router.delete(
    '/{stop_word}',
    response_model=StopwordDB,
    dependencies=[Depends(current_superuser)],
)
async def remove_stop_word(
    stop_word: str,
    session: AsyncSession = Depends(get_async_session),
):
    """Удаление стоп-слова. Только для суперюзеров."""
    stop_word = await check_word_exists(
        session, stop_word, stop_word_crud, 'Стоп-слово'
    )
    return await stop_word_crud.remove(stop_word, session)
