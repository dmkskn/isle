import isle._urls as URL

from ._requests import GET, GET_pages
from ._config import tmdb_api_key
from .objects import Movie


__all__ = [
    "get_latest",
    "get_popular",
    "get_top_rated",
    # "get_now_playing",
    # "get_upcoming",
]


def get_latest(**kwargs):
    """Get the most newly created movie. This is a live response
    and will continuously change."""
    params = {"api_key": tmdb_api_key(), **kwargs}
    item = GET(URL.MOVIE_GET_LATEST, **params)
    return Movie(item["id"], **item)


def get_popular(**kwargs):
    """Get the popular movies on TMDb. This list
    updates daily.

    Returns a generator. Each item is a `Movie` object."""
    params = {"api_key": tmdb_api_key(), **kwargs}
    for item in GET_pages(URL.MOVIE_GET_POPULAR, params):
        yield Movie(item["id"], **item)


def get_top_rated(**kwargs):
    """Get the top rated movies on TMDb.

    Returns a generator. Each item is a `Movie` object."""
    params = {"api_key": tmdb_api_key(), **kwargs}
    for item in GET_pages(URL.MOVIE_GET_TOP_RATED, params):
        yield Movie(item["id"], **item)


def get_now_playing(**kwargs):
    """Get movies in theatres.

    You can optionally specify a region parameter which will narrow
    the search to only look for theatrical release dates within the
    specified country.

    Returns a generator. Each item is a `Movie` object."""
    params = {"api_key": tmdb_api_key(), **kwargs}
    for item in GET_pages(URL.MOVIE_GET_NOW_PLAYING, params):
        yield Movie(item["id"], **item)


def get_upcoming(**kwargs):
    """Get upcoming movies in theatres.

    You can optionally specify a region parameter which will narrow
    the search to only look for theatrical release dates within
    the specified country.

    Returns a generator. Each item is a `Movie` object."""
    params = {"api_key": tmdb_api_key(), **kwargs}
    for item in GET_pages(URL.MOVIE_GET_UPCOMING, params):
        yield Movie(item["id"], **item)
