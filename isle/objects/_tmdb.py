import copy
from abc import ABC, abstractmethod

import isle._urls as URL

from .._config import tmdb_api_key
from .._requests import DELETE, GET, POST, GET_pages


class TMDb(ABC):
    def __init__(self, tmdb_id: int, **kwargs):
        self.data = {"id": tmdb_id, **kwargs}
        self.tmdb_id = self.data["id"]
        self.n_requests = 0

    @abstractmethod
    def _init(self):
        pass

    def _getdata(self, key):
        if key not in self.data:
            self._init()
        return copy.deepcopy(self.data[key])

    def _request(self, url: str, **params):
        self.n_requests += 1
        return GET(url, **{"api_key": tmdb_api_key(), **params})

    def _iter_request(self, url: str, **params):
        self.n_requests += 1
        return GET_pages(url, {"api_key": tmdb_api_key(), **params})

    def _post_request(self, url, data, **params):
        params = {"api_key": tmdb_api_key(), **params}
        request = POST(url, data, **params)
        self.n_requests += 1
        return request

    def _delete_request(self, url, data, **params):
        params = {"api_key": tmdb_api_key(), **params}
        request = DELETE(url, data, **params)
        self.n_requests += 1
        return request

    def _get_all_languages(self):
        data = self._request(
            URL.LANGUAGES_CONFIGURATION, **{"api_key": tmdb_api_key()}
        )
        languages = {}
        for item in data:
            iso_639_1 = item["iso_639_1"]
            del item["iso_639_1"]
            languages[iso_639_1] = item
        return languages

    def __repr__(self):
        return f"{type(self).__name__}({self.tmdb_id})"
