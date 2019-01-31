import isle._urls as URL

from ._config import tmdb_api_key
from ._requests import GET, GET_pages
from .objects import Person


__all__ = ["get_popular", "get_latest"]


def get_popular(**kwargs):
    """Get the current popular people on TMDb. This list updates
    daily.

    Returns a generator. Each item is a `Show` object."""
    params = {"api_key": tmdb_api_key(), **kwargs}
    for item in GET_pages(URL.PERSON_GET_POPULAR, params):
        yield Person(item["id"], **item)


def get_latest(**kwargs):
    """Get the most newly created person. This is a live response
    and will continuously change."""
    params = {"api_key": tmdb_api_key(), **kwargs}
    item = GET(URL.PERSON_GET_LATEST, **params)
    return Person(item["id"], **item)
