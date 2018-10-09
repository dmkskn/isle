import os
from urllib.parse import urljoin

from ._tools import search_results_for as _search_results_for
from ._objects import Movie, Show, Person, Company
from .config import TMDB_API_KEY
from ._urls import (
    BASEURL,
    SEARCH_MOVIE_SUFFIX,
    SEARCH_SHOW_SUFFIX,
    SEARCH_PERSON_SUFFIX,
    SEARCH_COMPANY_SUFFIX,
    DISCOVER_MOVIES_SUFFIX,
    DISCOVER_SHOWS_SUFFIX,
)


__all__ = [
    "search_movie",
    "search_show",
    "search_person",
    "search_company",
    "discover_movies",
    "discover_shows",
]


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
    url = urljoin(BASEURL, SEARCH_MOVIE_SUFFIX)
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
    url = urljoin(BASEURL, SEARCH_SHOW_SUFFIX)
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
    url = urljoin(BASEURL, SEARCH_PERSON_SUFFIX)
    params = {"query": query, "api_key": TMDB_API_KEY, **kwargs}
    for item in _search_results_for(url, params):
        yield Person(**item)


def search_company(query: str, **kwargs):
    """Search for companies.

    The `query` argument is a text query to search (required).

    Returns a generator. Each item is a `Company` object.
    """
    url = urljoin(BASEURL, SEARCH_COMPANY_SUFFIX)
    params = {"query": query, "api_key": TMDB_API_KEY, **kwargs}
    for item in _search_results_for(url, params):
        yield Company(**item)


def discover_movies(options: dict):
    """Discover movies by different types of data like
    average rating, number of votes, genres and certifications.

    See available options: 
    https://developers.themoviedb.org/3/discover/movie-discover
    
    Returns a generator. Each item is a `Movie` object.
    """
    url = urljoin(BASEURL, DISCOVER_MOVIES_SUFFIX)
    params = {"api_key": TMDB_API_KEY, **options}
    for item in _search_results_for(url, params):
        yield Movie(**item)


def discover_shows(options: dict):
    """Discover TV shows by different types of data like
    average rating, number of votes, genres, the network
    they aired on and air dates.

    See available options: 
    https://developers.themoviedb.org/3/discover/tv-discover
    
    Returns a generator. Each item is a `Show` object.
    """
    url = urljoin(BASEURL, DISCOVER_SHOWS_SUFFIX)
    params = {"api_key": TMDB_API_KEY, **options}
    for item in _search_results_for(url, params):
        yield Show(**item)
