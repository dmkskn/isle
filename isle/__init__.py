"""A wrapper for The Movie Database API"""
import os

from .objects import *
from ._api import *


__all__ = _api.__all__ + objects.__all__  # pylint: disable=E0602


TMDB_API_KEY = os.environ.get("TMDB_API_KEY", None)
del os
