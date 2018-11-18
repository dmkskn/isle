import os
from urllib.parse import urljoin
from collections import defaultdict
from ._tools import search_results_for as _search_results_for
from ._tools import get_response
from ._objects import Movie, Show, Person, Company, Episode, Season
from ._urls import (
    BASEURL,
    SEARCH_MOVIE_SUFFIX,
    SEARCH_SHOW_SUFFIX,
    SEARCH_PERSON_SUFFIX,
    SEARCH_COMPANY_SUFFIX,
    DISCOVER_MOVIES_SUFFIX,
    DISCOVER_SHOWS_SUFFIX,
    FIND_SUFFIX,
    MOVIE_CERTIFICATION_SUFFIX,
    SHOW_CERTIFICATION_SUFFIX,
    MOVIE_GENRES_SUFFIX,
    SHOW_GENRES_SUFFIX,
    IMAGE_CONFIGURATION_SUFFIX,
    COUNTRIES_CONFIGURATION_SUFFIX,
    JOBS_CONFIGURATION_SUFFIX,
    LANGUAGES_CONFIGURATION_SUFFIX,
    PRIMARY_TRANSLATIONS_CONFIGURATION_SUFFIX,
    TIMEZONES_CONFIGURATION_SUFFIX,
)


__all__ = [
    "search_movie",
    "search_show",
    "search_person",
    "search_company",
    "discover_movies",
    "discover_shows",
    "find",
    "get_movie_certifications",
    "get_show_certifications",
    "get_movie_genres",
    "get_show_genres",
    "get_image_configurations",
    "get_countries",
    "get_jobs",
    "get_languages",
    "get_primary_translations",
    "get_timezones",
]


def _get_tmdb_api_key():
    from . import TMDB_API_KEY

    return TMDB_API_KEY


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
    params = {"query": query, "api_key": _get_tmdb_api_key(), **kwargs}
    for item in _search_results_for(url, params):
        yield Movie(item["id"], **item)


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
    params = {"query": query, "api_key": _get_tmdb_api_key(), **kwargs}
    for item in _search_results_for(url, params):
        yield Show(item["id"], **item)


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
    params = {"query": query, "api_key": _get_tmdb_api_key(), **kwargs}
    for item in _search_results_for(url, params):
        yield Person(item["id"], **item)


def search_company(query: str, **kwargs):
    """Search for companies.

    The `query` argument is a text query to search (required).

    Returns a generator. Each item is a `Company` object.
    """
    url = urljoin(BASEURL, SEARCH_COMPANY_SUFFIX)
    params = {"query": query, "api_key": _get_tmdb_api_key(), **kwargs}
    for item in _search_results_for(url, params):
        yield Company(item["id"], **item)


def discover_movies(options: dict):
    """Discover movies by different types of data like
    average rating, number of votes, genres and certifications.

    See available options:
    https://developers.themoviedb.org/3/discover/movie-discover

    Returns a generator. Each item is a `Movie` object.
    """
    url = urljoin(BASEURL, DISCOVER_MOVIES_SUFFIX)
    params = {"api_key": _get_tmdb_api_key(), **options}
    for item in _search_results_for(url, params):
        yield Movie(item["id"], **item)


def discover_shows(options: dict):
    """Discover TV shows by different types of data like
    average rating, number of votes, genres, the network
    they aired on and air dates.

    See available options:
    https://developers.themoviedb.org/3/discover/tv-discover

    Returns a generator. Each item is a `Show` object.
    """
    url = urljoin(BASEURL, DISCOVER_SHOWS_SUFFIX)
    params = {"api_key": _get_tmdb_api_key(), **options}
    for item in _search_results_for(url, params):
        yield Show(item["id"], **item)


def find(external_id: str, *, src: str, **options):
    """Search for objects by an external id.

    Allowed sources (`src`): `imdb_id`, `freebase_mid`,
    `freebase_id`, `tvdb_id`, `tvrage_id`

    See available options:
    https://developers.themoviedb.org/3/find/find-by-id
    """
    url = urljoin(BASEURL, FIND_SUFFIX.format(external_id))
    params = {"api_key": _get_tmdb_api_key(), "external_source": src, **options}
    response = get_response(url, **params)
    acc = {}
    for key, results in response.items():
        if key == "movie_results":
            acc[key] = [Movie(x["id"], **x) for x in results]
        elif key == "person_results":
            acc[key] = [Person(x["id"], **x) for x in results]
        elif key == "tv_results":
            acc[key] = [Show(x["id"], **x) for x in results]
        elif key == "tv_episode_results":
            for x in results:
                n = x["episode_number"]
                sn = x["season_number"]
                show_id = x["show_id"]
                del x["episode_number"]
                del x["season_number"]
                del x["show_id"]
                acc.setdefault(key, []).append(
                    Episode(n, show_id=show_id, season_number=sn, **x)
                )
        elif key == "tv_season_results":
            for x in results:
                n = x["season_number"]
                show_id = x["show_id"]
                del x["season_number"]
                del x["show_id"]
                acc.setdefault(key, []).append(Season(n, show_id=show_id, **x))
        else:
            raise ValueError(f"Unkown type: {key}")
    return acc


def get_movie_certifications():
    """Get an up to date list of the officially supported
    movie certifications on TMDb."""
    url = urljoin(BASEURL, MOVIE_CERTIFICATION_SUFFIX)
    return get_response(url, **{"api_key": _get_tmdb_api_key()})["certifications"]


def get_show_certifications():
    """Get an up to date list of the officially supported TV
    show certifications on TMDb."""
    url = urljoin(BASEURL, SHOW_CERTIFICATION_SUFFIX)
    return get_response(url, **{"api_key": _get_tmdb_api_key()})["certifications"]


def get_movie_genres():
    """Get the list of official genres for movies."""
    url = urljoin(BASEURL, MOVIE_GENRES_SUFFIX)
    return get_response(url, **{"api_key": _get_tmdb_api_key()})["genres"]


def get_show_genres():
    """Get the list of official genres for TV shows."""
    url = urljoin(BASEURL, SHOW_GENRES_SUFFIX)
    return get_response(url, **{"api_key": _get_tmdb_api_key()})["genres"]


def get_image_configurations():
    """Get the data relevant to building image URLs as well
    as the change key map."""
    url = urljoin(BASEURL, IMAGE_CONFIGURATION_SUFFIX)
    return get_response(url, **{"api_key": _get_tmdb_api_key()})


def get_countries():
    """Get the list of countries (ISO 3166-1 tags) used
    throughout TMDb."""
    url = urljoin(BASEURL, COUNTRIES_CONFIGURATION_SUFFIX)
    return get_response(url, **{"api_key": _get_tmdb_api_key()})


def get_jobs():
    """Get a list of the jobs and departments we use on
    TMDb."""
    url = urljoin(BASEURL, JOBS_CONFIGURATION_SUFFIX)
    return get_response(url, **{"api_key": _get_tmdb_api_key()})


def get_languages():
    """Get the list of languages (ISO 639-1 tags) used
    throughout TMDb."""
    url = urljoin(BASEURL, LANGUAGES_CONFIGURATION_SUFFIX)
    return get_response(url, **{"api_key": _get_tmdb_api_key()})


def get_primary_translations():
    """Get a list of the officially supported translations
    on TMDb."""
    url = urljoin(BASEURL, PRIMARY_TRANSLATIONS_CONFIGURATION_SUFFIX)
    return get_response(url, **{"api_key": _get_tmdb_api_key()})


def get_timezones():
    """Get the list of timezones used throughout TMDb."""
    url = urljoin(BASEURL, TIMEZONES_CONFIGURATION_SUFFIX)
    return get_response(url, **{"api_key": _get_tmdb_api_key()})
