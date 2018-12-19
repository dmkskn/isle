from typing import Iterator, List, NamedTuple, Optional, Union
from importlib import import_module

import isle._urls as URL
from ._tmdb import TMDb
from .._config import tmdb_api_key
from .._requests import GET


__all__ = [
    "Keyword",
    "Genre",
    "Image",
    "Country",
    "Language",
    "Vote",
    "Video",
    "Credit",
]


def _import_movie():
    global Movie
    Movie = import_module("isle.objects._movie").Movie


def _import_show():
    global Show
    Show = import_module("isle.objects._show").Show


def _import_person():
    global Person
    Person = import_module("isle.objects._person").Person


def _import_all():
    _import_movie()
    _import_show()
    _import_person()


class Keyword(TMDb):
    """Represents a keyword."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        _import_all()

    def _init(self):
        self.get_details()

    @property
    def name(self):
        """Return a keyword's name"""
        return self._getdata("name")

    def get_details(self):
        """Get the primary information about a keyword."""
        details = self._request(
            URL.KEYWORD_DETAILS.format(keyword_id=self.tmdb_id)
        )
        self.data.update(details)
        return details

    def iter_movies(self, **params):
        """Get the movies that belong to a keyword."""
        results = self._iter_request(
            URL.KEYWORD_MOVIES.format(keyword_id=self.tmdb_id), **params
        )
        yield from map(lambda x: Movie(x["id"]), results)

    def __str__(self):
        return self._getdata("name")


class Genre(NamedTuple):
    """Represents a genre."""

    tmdb_id: str
    name: str

    def __str__(self):
        return self.name


class Image:
    """Represents an image."""

    def __init__(self, image: dict, *, type_: str):
        assert type_ in ["backdrop", "poster", "logo", "profile", "still"]
        self._type = type_
        self._configs_data = {}
        for key in image.keys() - {"vote_average", "vote_count"}:
            setattr(self, key, image[key])
        if {"vote_average", "vote_count"} <= image.keys():
            self.vote = Vote(
                average=image["vote_average"], count=image["vote_count"]
            )

    @property
    def _configs(self):
        if not self._configs_data:
            self._configs_data.update(self._get_image_configs())
        return self._configs_data

    @property
    def url(self):
        urls = {}
        base = self._configs["secure_base_url"]
        for size in self.sizes:
            urls[size] = f"{base}/{size}{self.file_path}"
        return urls

    @property
    def sizes(self):
        return self._configs[self._image_sizes_key]

    @property
    def _image_sizes_key(self):
        if self._type == "backdrop":
            return "backdrop_sizes"
        elif self._type == "poster":
            return "poster_sizes"
        elif self._type == "logo":
            return "logo_sizes"
        elif self._type == "profile":
            return "profile_sizes"
        elif self._type == "still":
            return "still_sizes"
        else:
            raise ValueError(f"Unknown image type: {self._type}")

    def _get_image_configs(self):
        res = GET(URL.IMAGE_CONFIGURATION, **{"api_key": tmdb_api_key()})[
            "images"
        ]
        return res

    def __repr__(self):
        return f"Image(height={self.height}, width={self.width}, _type={self._type})"


class Country(NamedTuple):
    """Represents a country."""

    iso_3166_1: str
    english_name: str

    def __str__(self):
        return self.english_name


class Language(NamedTuple):
    """Represents a language."""

    iso_639_1: str
    english_name: str
    original_name: str

    def __str__(self):
        return self.english_name


class Vote(NamedTuple):
    """Represents a vote."""

    average: float
    count: str

    def __str__(self):
        return self.average


class Video(NamedTuple):
    """Represents a video."""

    name: str
    type: str
    url: str

    def __str__(self):
        return self.url


class Credit(TMDb):
    """Represents a credit."""

    def __init__(self, tmdb_id, **kwargs):
        _import_all()
        self.data = {"credit_id": tmdb_id, **kwargs}
        self.tmdb_id = self.data["credit_id"]
        self._person_data = kwargs.get("person_data")
        self._media_data = kwargs.get("media_data")
        self._character = kwargs.get("character")
        self.n_requests = 0

    def _init(self):
        self.get_details()

    @property
    def type(self):
        """Return a credit type"""
        return self._getdata("credit_type")

    @property
    def media_type(self):
        """Return a media type"""
        return self._getdata("media_type")

    @property
    def department(self):
        return self._getdata("department")

    @property
    def job(self):
        return self._getdata("job")

    @property
    def character(self):
        if self.type == "crew":
            return None
        return self._character or self._getdata("media")["character"]

    @property
    def person(self):
        data = self._person_data or self._getdata("person")
        return Person(data["id"], **data)

    @property
    def person_known_for(self):
        media = []
        for item in self._getdata("person")["known_for"]:
            Obj = Show if item["media_type"] == "tv" else Movie
            media.append(Obj(item["id"], **item))
        return media

    @property
    def media(self):
        Obj = Show if self.media_type == "tv" else Movie
        if self._media_data:
            data = self._media_data
        else:
            data = self._getdata("media")
            data.pop("seasons", None)
            data.pop("episodes", None)
        return Obj(data["id"], **data)

    def get_details(self):
        """Get a movie or TV credit details."""
        details = self._request(
            URL.CREDIT_DETAILS.format(credit_id=self.tmdb_id)
        )
        self.data.update(details)
        return details
