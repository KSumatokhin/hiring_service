from app.models import Stopword
from app.crud import WordCRUDBase


stop_word_crud = WordCRUDBase(Stopword)
