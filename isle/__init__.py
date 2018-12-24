"""A wrapper for The Movie Database API"""
import os

import isle._api

from .objects import *
from ._api import *


__all__ = isle._api.__all__


TMDB_API_KEY = os.environ.get("TMDB_API_KEY", None)
del os
