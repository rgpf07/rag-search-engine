import string
from functools import lru_cache
from typing import Any

from nltk.stem import PorterStemmer

from .utils import DEFAULT_SEARCH_LIMIT, load_movies, load_stopwords


def search_command(
    query: str, limit: int = DEFAULT_SEARCH_LIMIT
) -> list[dict[str, Any]]:
    movies = load_movies()
    matched = []
    query_tokens = tokenize_text(query)
    for movie in movies:
        title_tokens = tokenize_text(movie.get("title", ""))
        if has_matching_query(query_tokens, title_tokens):
            matched.append(movie)
        if len(matched) >= limit:
            break
    return matched


def preprocess_text(text: str) -> str:
    table = str.maketrans("", "", string.punctuation)
    processed_text = text.translate(table)
    return processed_text.lower()


def tokenize_text(text: str) -> list[str]:
    text = preprocess_text(text)
    stopwords = _stopword_set()
    tokens = remove_stopwords(text.split(), stopwords)
    valid_tokens = []
    stemmer = PorterStemmer()
    for token in tokens:
        if token:
            valid_tokens.append(stemmer.stem(token))

    return valid_tokens


def has_matching_query(query_tokens: list[str], title_tokens: list[str]) -> bool:
    for query_token in query_tokens:
        for title_token in title_tokens:
            if query_token in title_token:
                return True
    return False


def remove_stopwords(words: list[str], stopwords: frozenset[str]) -> list[str]:
    filtered = []
    for word in words:
        if word not in stopwords:
            filtered.append(word)
    return filtered


@lru_cache
def _stopword_set() -> frozenset[str]:
    return frozenset(word.casefold() for word in load_stopwords())
