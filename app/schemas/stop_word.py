from pydantic import (
    BaseModel,
    ConfigDict,
    Field
)

from app.core.db import MAX_LENGHT


class StopwordCreate(BaseModel):
    word: str = Field(..., max_length=MAX_LENGHT)
    model_config = ConfigDict(extra='forbid', from_attributes=True)


class StopWordsCreateList(BaseModel):
    words: list[str]
    model_config = ConfigDict(extra='forbid', from_attributes=True)


class StopwordDB(StopwordCreate):
    id: int
