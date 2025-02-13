from pydantic import (
    BaseModel,
    ConfigDict,
    Field
)

from app.core.db import MAX_LENGHT


class KeywordCreate(BaseModel):
    word: str = Field(..., max_length=MAX_LENGHT)
    model_config = ConfigDict(extra='forbid', from_attributes=True)


class KeyWordsCreateList(BaseModel):
    words: list[str]
    model_config = ConfigDict(extra='forbid', from_attributes=True)


class KeywordDB(KeywordCreate):
    id: int
