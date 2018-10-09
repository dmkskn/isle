from abc import ABC, abstractmethod

from ._tools import get_response
from .config import TMDB_API_KEY
from ._urls import (
    BASEURL,
)


class _BaseTMDbObject(ABC):
    def __init__(self, **kwargs):
        self.tmdb_id = kwargs["id"]
        if kwargs.get("__is_first_init__", False):
            self._set_attrs(**kwargs)
        else:
            self._first_init()

    @abstractmethod
    def _first_init(self):
        pass

    def _set_attrs(self, **kwargs):
        for key in kwargs.keys() - {"id", "__is_first_init__"}:
            setattr(self, key, kwargs[key])

    def _request(self, url: str, **params) -> dict:
        return get_response(url, **{"api_key": TMDB_API_KEY, **params})


class Movie:
    def __init__(self, tmdb_id=None, **kwargs):
        self.tmdb_id = tmdb_id or kwargs["id"]
        for key in kwargs.keys() - {"id"}:
            setattr(self, key, kwargs[key])



class Show:
    def __init__(self, tmdb_id=None, **kwargs):
        self.tmdb_id = tmdb_id or kwargs["id"]
        for key in kwargs.keys() - {"id"}:
            setattr(self, key, kwargs[key])



class Person:
    def __init__(self, tmdb_id=None, **kwargs):
        self.tmdb_id = tmdb_id or kwargs["id"]
        for key in kwargs.keys() - {"id"}:
            setattr(self, key, kwargs[key])



class Company:
    def __init__(self, tmdb_id=None, **kwargs):
        self.tmdb_id = tmdb_id or kwargs["id"]
        for key in kwargs.keys() - {"id"}:
            setattr(self, key, kwargs[key])
