import os
import json
from urllib.parse import urljoin, urlencode
from urllib.request import urlopen

from ._objects import Movie, Show, Person, Company


__all__ = ["search_movie", "search_show", "search_person", "search_company"]


_BASEURL = "https://api.themoviedb.org/"
_SEARCH_MOVIE_SUFFIX = "3/search/movie"
_SEARCH_SHOW_SUFFIX = "3/search/tv"
_SEARCH_PERSON_SUFFIX = "3/search/person"
_SEARCH_COMPANY_SUFFIX = "3/search/company"

TMDB_API_KEY = os.environ.get("TMDB_API_KEY", None)



def search_movie(query: str, **kwargs):
    """Search for movies.

    The `query` argument is a text query to search (required).

    The optional `year` argument specifies the release year of 
    the movie.

    The optional `language` argument specifies a ISO 639-1 code
    to display translated data for the fields that support it.
    (Default: "en-US")

    The optional `include_adult` argument specifies whether
    to include adult (pornography) content in the results.
    (Default: False)

    The optional `region` argument specifies a ISO 3166-1 code
    to filter release dates. Must be uppercase.

    Returns a generator. Each item is a `Movie` object.
    """
    url = urljoin(_BASEURL, _SEARCH_MOVIE_SUFFIX)
    params = {"query": query, "api_key": TMDB_API_KEY, **kwargs}
    for item in _search_results_for(url, params):
        yield Movie(**item)


def search_show(query: str, **kwargs):
    """Search for TV shows.

    The `query` argument is a text query to search (required).

    The optional `language` argument specifies a ISO 639-1 code
    to display translated data for the fields that support it.
    (Default: "en-US")

    The optional `first_air_date_year` argument specifies 
    the year when the show was first aired.

    Returns a generator. Each item is a `Show` object.
    """
    url = urljoin(_BASEURL, _SEARCH_SHOW_SUFFIX)
    params = {"query": query, "api_key": TMDB_API_KEY, **kwargs}
    for item in _search_results_for(url, params):
        yield Show(**item)


def search_person(query: str, **kwargs):
    """Search for people.

    The `query` argument is a text query to search (required).

    The optional `language` argument specifies a ISO 639-1 code
    to display translated data for the fields that support it.
    (Default: "en-US")

    The optional `include_adult` argument specifies whether
    to include adult (pornography) content in the results.
    (Default: False)

    The optional `region` argument specifies a ISO 3166-1 code
    to filter release dates. Must be uppercase.

    Returns a generator. Each item is a `Person` object.
    """
    url = urljoin(_BASEURL, _SEARCH_PERSON_SUFFIX)
    params = {"query": query, "api_key": TMDB_API_KEY, **kwargs}
    for item in _search_results_for(url, params):
        yield Person(**item)


def search_company(query: str, **kwargs):
    """Search for companies.

    The `query` argument is a text query to search (required).

    Returns a generator. Each item is a `Company` object.
    """
    url = urljoin(_BASEURL, _SEARCH_COMPANY_SUFFIX)
    params = {"query": query, "api_key": TMDB_API_KEY, **kwargs}
    for item in _search_results_for(url, params):
        yield Company(**item)


def _search_results_for(url: str, params: dict):
    def get_page(url, *, page, **params):
        params = urlencode({**params, 'page': page})
        response = urlopen(f"{url}?{params}")
        return json.loads(response.read().decode("utf-8"))
    
    def get_total_pages_for(url, params):
        first_page = get_page(url, page=1, **params)
        return first_page["total_pages"] 

    for page in range(1, get_total_pages_for(url, params) + 1):
        yield from get_page(url, page=page, **params)["results"]