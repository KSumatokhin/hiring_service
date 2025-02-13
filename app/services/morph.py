import re
import string

import spacy


nlp_ru = spacy.load('ru_core_news_sm')
nlp_en = spacy.load('en_core_web_sm')

STOP_RU = nlp_ru.Defaults.stop_words
STOP_EN = nlp_en.Defaults.stop_words
STOP_WORDS = STOP_RU.union(STOP_EN)


def is_cyrillic(text: str) -> bool:
    """Определяет на кириллице или латинице написан текст."""
    return bool(re.search('[а-яА-Я]', text))


def tokenize_text(text: str) -> list[str]:
    """Удаляет из текста знаки препинания и разбивает на слова."""
    cleaned_text = ''.join(
        [char.lower() for char in text if char not in string.punctuation]
    )
    return re.findall(r'\b\w+\b', cleaned_text)


def delete_stopwords(tokens: list[str]) -> list[str]:
    """Удаляет стоп-слова из списка."""
    return [token for token in tokens if token not in STOP_WORDS]


def lemmatize_word(word: str) -> str:
    """Переводит слово в нормальную форму."""
    if is_cyrillic(word):
        doc = nlp_ru(word)
    else:
        doc = nlp_en(word)

    return doc[0].lemma_


def lemmatize_tokens(tokens: list[str]) -> list[str]:
    """Приводит слова в списке к нормальной форме."""
    return [lemmatize_word(token) for token in tokens]


def process_text_pipeline(
    text: str, delete_stop_words: bool = False
) -> list[str]:
    """
    Обработка текста.
    Токенизирует, удаляет стоп-слова, лемматизирует
    и возвращает итоговый список лемм.
    """
    tokens = tokenize_text(text)
    if delete_stop_words:
        tokens = delete_stopwords(tokens)
    lemmas = lemmatize_tokens(tokens)
    return lemmas
