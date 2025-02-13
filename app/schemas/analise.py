from pydantic import (
    BaseModel,
    ConfigDict,
    Field
)

from app.core.db import MAX_LENGHT


class Words(BaseModel):
    key_words: list[str] = Field(..., max_length=MAX_LENGHT)
    stop_words: list[str] = Field(..., max_length=MAX_LENGHT)
    model_config = ConfigDict(extra='forbid', from_attributes=True)
