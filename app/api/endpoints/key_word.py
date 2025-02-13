from http import HTTPStatus

from fastapi import (
    APIRouter, Depends, File, HTTPException, UploadFile
)
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import (
    check_word_duplicate,
    check_word_exists,
)
from app.core.db import get_async_session
from app.core.user import current_superuser
from app.crud import key_word_crud
from app.schemas.key_word import (
    KeyWordsCreateList,
    KeywordCreate,
    KeywordDB,
)
from app.models.key_word import Keyword
from app.services.morph import lemmatize_word


router = APIRouter()


@router.get(
    '/',
    response_model=list[str],
)
async def get_all_keywords(
    session: AsyncSession = Depends(get_async_session),
):
    """Список всех ключевых слов."""
    return await key_word_crud.get_all_words(session)


@router.post(
    '/',
    response_model=KeywordDB,
    dependencies=[Depends(current_superuser)],
)
async def create_new_key_word(
    key_word: KeywordCreate,
    session: AsyncSession = Depends(get_async_session),
):
    """Создание ключевого слова. Только для суперюзеров."""
    key_word.word = lemmatize_word(key_word.word.lower())
    key_word_id = await check_word_duplicate(
        session, key_word.word, key_word_crud
    )
    if key_word_id:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Такое ключевое слово уже существует!'
        )
    return await key_word_crud.create(key_word, session)


@router.post(
        '/batch', response_model=list[KeywordDB],
        dependencies=[Depends(current_superuser)]
    )
async def create_key_words_batch(
    words_in: KeyWordsCreateList,
    session: AsyncSession = Depends(get_async_session),
):
    """Создание нескольких ключевых слов за один раз."""
    created_objs = []
    to_create = []
    exists_obj = []
    for word in words_in.words:
        lemma = lemmatize_word(word.lower())
        key_word_id = await check_word_duplicate(
            session, lemma, key_word_crud
        )
        if key_word_id:
            exists_obj.append(
                Keyword(id=key_word_id, word=f'{lemma} уже существует')
            )
        else:
            to_create.append(KeywordCreate(word=lemma))
    created_objs = await key_word_crud.create_multi(to_create, session)
    created_objs.extend(exists_obj)
    return created_objs


@router.delete(
    '/{key_word}',
    response_model=KeywordDB,
    dependencies=[Depends(current_superuser)],
)
async def remove_key_word(
    key_word: str,
    session: AsyncSession = Depends(get_async_session),
):
    """Удаление ключевого слова. Только для суперюзеров."""
    key_word = await check_word_exists(
        session, key_word, key_word_crud, 'Ключевое слово'
    )
    return await key_word_crud.remove(key_word, session)


@router.post(
        '/upload-file', response_model=list[KeywordDB],
        dependencies=[Depends(current_superuser)]
    )
async def upload_key_words_file(
    file: UploadFile = File(...),
    session: AsyncSession = Depends(get_async_session),
):
    lines = (await file.read()).decode('utf-8').splitlines()
    created_objs = []
    to_create = []
    exists_obj = []
    for line in lines:
        cleaned = line.strip()
        if not cleaned:
            continue
        lemma = lemmatize_word(cleaned.lower())
        key_word_id = await check_word_duplicate(
            session, lemma, key_word_crud
        )
        if key_word_id:
            exists_obj.append(
                Keyword(id=key_word_id, word=f'{lemma} уже существует')
            )
        else:
            to_create.append(KeywordCreate(word=lemma))
    created_objs = await key_word_crud.create_multi(to_create, session)
    created_objs.extend(exists_obj)
    return created_objs
