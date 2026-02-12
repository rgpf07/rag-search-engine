import string
from functools import lru_cache
from typing import Any, Callable

from nltk.stem import PorterStemmer

from .utils import DEFAULT_SEARCH_LIMIT, load_movies, load_stopwords

TextFn = Callable[[str], str]
TokenFn = Callable[[list[str]], list[str]]


@lru_cache
def _stopword_set() -> frozenset[str]:
    return frozenset(word.casefold() for word in load_stopwords())


def compose_text(*funcs: TextFn) -> TextFn:
    def _run(x: str) -> str:
        for fn in funcs:
            x = fn(x)
        return x

    return _run


def compose_tokens(*funcs: TokenFn) -> TokenFn:
    def _run(tokens: list[str]) -> list[str]:
        for fn in funcs:
            tokens = fn(tokens)
        return tokens

    return _run


@lru_cache
def build_preprocessor(stopwords: frozenset[str]) -> Callable[[str], list[str]]:
    table = str.maketrans("", "", string.punctuation)
    stemmer = PorterStemmer()

    def lower_case(text: str) -> str:
        return text.lower()

    def strip_punct(text: str) -> str:
        return text.translate(table)

    text_pipeline = compose_text(lower_case, strip_punct)

    def split_words(text: str) -> list[str]:
        return text.split()

    def remove_stopwords(tokens: list[str]) -> list[str]:
        valid = []
        for token in tokens:
            if token and token not in stopwords:
                valid.append(token)
        return valid

    def stem(tokens: list[str]) -> list[str]:
        return [stemmer.stem(token) for token in tokens]

    token_pipeline = compose_tokens(remove_stopwords, stem)

    def preprocess(text: str) -> list[str]:
        normalized = text_pipeline(text)
        tokens = split_words(normalized)
        return token_pipeline(tokens)

    return preprocess


preprocess = build_preprocessor(_stopword_set())


def search_command(
    query: str, limit: int = DEFAULT_SEARCH_LIMIT
) -> list[dict[str, Any]]:
    movies = load_movies()
    matched = []
    query_tokens = set(preprocess(query))
    for movie in movies:
        title_tokens = preprocess(movie.get("title", ""))
        if not query_tokens.isdisjoint(title_tokens):
            matched.append(movie)
        if len(matched) >= limit:
            break
    return matched
