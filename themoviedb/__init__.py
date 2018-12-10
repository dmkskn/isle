import os

from ._api import *
from .objects.account import *
from .objects.movie import *
from .objects.show import *
from .objects.person import *
from .objects.company import *


TMDB_API_KEY = os.environ.get("TMDB_API_KEY", None)
