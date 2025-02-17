import csv

from fastapi import APIRouter, Depends, File, Request, UploadFile
from fastapi.responses import RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.models.key_word import Keyword
from app.schemas.key_word import KeywordCreate


router = APIRouter(prefix='/admin')


@router.post("/upload_csv", name="upload_csv")
async def upload_csv(
    request: Request,
    file: UploadFile,
    # key_word: KeywordCreate,
    session: AsyncSession = Depends(get_async_session)
):
    contents = await file.read()
    reader = csv.DictReader(contents.decode('utf-8').splitlines())
    for row in reader:
        keyword = row['word']
        # Подгрузить сюда keyword_crud и
        # сначала проверить наличие, затем добавлять, а не так как сейчас
        obj = Keyword(word=keyword)
        session.add(obj)
        await session.commit()
        await session.refresh(obj)
    # Перенаправляем обратно в админку
    return RedirectResponse(
        url=request.url_for(
            "admin:list",
            identity="keyword"
        ),
        status_code=303
    )
