import os
from collections import defaultdict
from urllib.parse import urljoin

from . import _urls as URL

from ._config import tmdb_api_key
from ._requests import GET, GET_pages
from .objects import (
    Company,
    Movie,
    Country,
    Genre,
    Language,
    Person,
    Episode,
    Season,
    Show,
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
    params = {"query": query, "api_key": tmdb_api_key(), **kwargs}
    for item in GET_pages(URL.SEARCH_MOVIE, params):
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
    params = {"query": query, "api_key": tmdb_api_key(), **kwargs}
    for item in GET_pages(URL.SEARCH_SHOW, params):
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
    params = {"query": query, "api_key": tmdb_api_key(), **kwargs}
    for item in GET_pages(URL.SEARCH_PERSON, params):
        yield Person(item["id"], **item)


def search_company(query: str, **kwargs):
    """Search for companies.

    The `query` argument is a text query to search (required).

    Returns a generator. Each item is a `Company` object.
    """
    params = {"query": query, "api_key": tmdb_api_key(), **kwargs}
    for item in GET_pages(URL.SEARCH_COMPANY, params):
        yield Company(item["id"], **item)


def discover_movies(options: dict):
    """Discover movies by different types of data like
    average rating, number of votes, genres and certifications.

    See available options:
    https://developers.themoviedb.org/3/discover/movie-discover

    Returns a generator. Each item is a `Movie` object.
    """
    params = {"api_key": tmdb_api_key(), **options}
    for item in GET_pages(URL.DISCOVER_MOVIES, params):
        yield Movie(item["id"], **item)


def discover_shows(options: dict):
    """Discover TV shows by different types of data like
    average rating, number of votes, genres, the network
    they aired on and air dates.

    See available options:
    https://developers.themoviedb.org/3/discover/tv-discover

    Returns a generator. Each item is a `Show` object.
    """
    params = {"api_key": tmdb_api_key(), **options}
    for item in GET_pages(URL.DISCOVER_SHOWS, params):
        yield Show(item["id"], **item)


def find(external_id: str, *, src: str, **options):
    """Search for objects by an external id.

    Allowed sources (`src`): `imdb_id`, `freebase_mid`,
    `freebase_id`, `tvdb_id`, `tvrage_id`

    See available options:
    https://developers.themoviedb.org/3/find/find-by-id
    """
    params = {"api_key": tmdb_api_key(), "external_source": src, **options}
    response = GET(URL.FIND.format(external_id=external_id), **params)
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


def get_movie_certifications(country=None):
    """Get an up to date list of the officially supported
    movie certifications on TMDb."""
    res = GET(URL.MOVIE_CERTIFICATION, **{"api_key": tmdb_api_key()})[
        "certifications"
    ]
    return res[country] if country else res


def get_show_certifications(country=None):
    """Get an up to date list of the officially supported TV
    show certifications on TMDb."""
    res = GET(URL.SHOW_CERTIFICATION, **{"api_key": tmdb_api_key()})[
        "certifications"
    ]
    return res[country] if country else res


def get_movie_genres(objects=False):
    """Get the list of official genres for movies."""
    genres = GET(URL.MOVIE_GENRES, **{"api_key": tmdb_api_key()})["genres"]
    if objects:
        return [Genre(tmdb_id=g["id"], name=g["name"]) for g in genres]
    else:
        return genres


def get_show_genres(objects=False):
    """Get the list of official genres for TV shows."""
    genres = GET(URL.SHOW_GENRES, **{"api_key": tmdb_api_key()})["genres"]
    if objects:
        return [Genre(tmdb_id=g["id"], name=g["name"]) for g in genres]
    else:
        return genres


def get_image_configurations():
    """Get the data relevant to building image URLs as well
    as the change key map."""
    return GET(URL.IMAGE_CONFIGURATION, **{"api_key": tmdb_api_key()})


def get_countries(objects=False):
    """Get the list of countries (ISO 3166-1 tags) used
    throughout TMDb."""
    countries = GET(URL.COUNTRIES_CONFIGURATION, **{"api_key": tmdb_api_key()})
    if objects:
        return [Country(**c) for c in countries]
    else:
        return countries


def get_jobs():
    """Get a list of the jobs and departments we use on
    TMDb."""
    return GET(URL.JOBS_CONFIGURATION, **{"api_key": tmdb_api_key()})


def get_languages(objects=False):
    """Get the list of languages (ISO 639-1 tags) used
    throughout TMDb."""
    languages = GET(URL.LANGUAGES_CONFIGURATION, **{"api_key": tmdb_api_key()})
    if objects:
        return [
            Language(
                iso_639_1=l["iso_639_1"],
                english_name=l["english_name"],
                original_name=l["name"],
            )
            for l in languages
        ]
    else:
        return languages


def get_primary_translations():
    """Get a list of the officially supported translations
    on TMDb."""
    return GET(
        URL.PRIMARY_TRANSLATIONS_CONFIGURATION, **{"api_key": tmdb_api_key()}
    )


def get_timezones():
    """Get the list of timezones used throughout TMDb."""
    return GET(URL.TIMEZONES_CONFIGURATION, **{"api_key": tmdb_api_key()})
