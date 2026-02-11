from typing import Any

from .utils import DEFAULT_SEARCH_LIMIT, load_movies


def search_command(
    query: str, limit: int = DEFAULT_SEARCH_LIMIT
) -> list[dict[str, Any]]:
    movies = load_movies()
    matched = []
    for movie in movies:
        title = movie.get("title", "")
        if isinstance(title, str) and query in title:
            matched.append(movie)
        if len(matched) >= limit:
            break
    return matched[:5]
