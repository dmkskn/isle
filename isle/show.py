import isle._urls as URL

from ._config import tmdb_api_key
from ._requests import GET, GET_pages
from .objects import Show


__all__ = [
    "get_latest",
    "get_airing_today",
    "get_on_the_air",
    "get_popular",
    "get_top_rated",
]


def get_latest(**kwargs):
    """Get the most newly created TV show. This is a live response
    and will continuously change."""
    params = {"api_key": tmdb_api_key(), **kwargs}
    item = GET(URL.SHOW_GET_LATEST, **params)
    return Show(item["id"], **item)


def get_airing_today(**kwargs):
    """Get TV shows that are airing today. This query is purely day
    based as we do not currently support airing times.

    Returns a generator. Each item is a `Show` object."""
    params = {"api_key": tmdb_api_key(), **kwargs}
    for item in GET_pages(URL.SHOW_GET_AIRING_TODAY, params):
        yield Show(item["id"], **item)


def get_on_the_air(**kwargs):
    """Get shows that are currently on the air. This query looks
    for any TV show that has an episode with an air date in the
    next 7 days.

    Returns a generator. Each item is a `Show` object."""
    params = {"api_key": tmdb_api_key(), **kwargs}
    for item in GET_pages(URL.SHOW_GET_ON_THE_AIR, params):
        yield Show(item["id"], **item)


def get_popular(**kwargs):
    """Get the current popular TV shows on TMDb. This list updates
    daily.

    Returns a generator. Each item is a `Show` object."""
    params = {"api_key": tmdb_api_key(), **kwargs}
    for item in GET_pages(URL.SHOW_GET_POPULAR, params):
        yield Show(item["id"], **item)


def get_top_rated(**kwargs):
    """Get the top rated TV shows on TMDb.

    Returns a generator. Each item is a `Show` object."""
    params = {"api_key": tmdb_api_key(), **kwargs}
    for item in GET_pages(URL.SHOW_GET_TOP_RATED, params):
        yield Show(item["id"], **item)
