from app.models import Keyword
from app.crud import WordCRUDBase


key_word_crud = WordCRUDBase(Keyword)
