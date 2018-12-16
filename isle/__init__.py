import os

from ._api import *
from .objects import *


TMDB_API_KEY = os.environ.get("TMDB_API_KEY", None)
del os
