import json
import os
from typing import Any

DEFAULT_SEARCH_LIMIT = 5

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
DATA_PATH = os.path.join(PROJECT_ROOT, "data", "movies.json")
STOPWORDS_PATH = os.path.join(PROJECT_ROOT, "data", "stopwords.txt")


def load_movies(path: str = DATA_PATH) -> list[dict[str, Any]]:
    with open(path, "r") as f:
        data = json.load(f)

    movies = data.get("movies", [])
    if not isinstance(movies, list):
        return []

    return movies


def load_stopwords(path: str = STOPWORDS_PATH) -> list[str]:
    with open(path, "r") as f:
        return f.read().splitlines()
