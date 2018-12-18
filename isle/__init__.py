import os

from .objects import *
from ._api import *


TMDB_API_KEY = os.environ.get("TMDB_API_KEY", None)
del os
