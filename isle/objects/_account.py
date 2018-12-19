import copy
from typing import NamedTuple
from importlib import import_module

import isle._urls as URL
from ._tmdb import TMDb
from .._config import tmdb_api_key


__all__ = ["Account", "TMDbList"]


def _import_movie():
    global Movie
    Movie = import_module("isle.objects._movie").Movie


def _import_show():
    global Show
    Show = import_module("isle.objects._show").Show


def _import_episode():
    global Episode
    Episode = import_module("isle.objects._show").Episode


def _import_language():
    global Language
    Language = import_module("isle.objects._others").Language


def _import_all():
    _import_movie()
    _import_show()
    _import_episode()
    _import_language()


class Account(TMDb):
    """Represents an user account."""

    class _Token(NamedTuple):
        id: str
        expires_at: str

    class _Session(NamedTuple):
        id: str
        is_guest: bool = False

    class SessionError(Exception):
        pass

    class TokenError(Exception):
        pass

    def __init__(self):
        _import_all()
        self.data = {}
        self._token = None
        self._session = None
        self.n_requests = 0

    def _init(self):
        self.get_details()

    def login(self, username, password):
        """Log in to the account."""
        self._create_token()
        self._validate_token(username, password)
        return self._create_session()

    def logout(self):
        """Logout from a session."""
        data = {"session_id": self._session_id}
        request = self._delete_request(URL.AUTH_DELETE_SESSION, data)
        self._token = self._session = None
        return request

    def login_as_guest(self):
        """Create a new guest session. Guest sessions are a type of
        session that will let a user rate movies and TV shows but
        not require them to have a TMDb user account. """
        request = self._request(URL.AUTH_GUEST_SESSION, api_key=tmdb_api_key())
        self._session = self._Session(
            id=request["guest_session_id"], is_guest=True
        )
        return request

    def _create_session(self):
        data = {"request_token": self._token_id}
        request = self._post_request(
            URL.AUTH_NEW_SESSION, data, api_key=tmdb_api_key()
        )
        self._session = self._Session(id=request["session_id"])
        return request

    def _create_token(self):
        """Create a temporary request token that can be used to
        validate a TMDb user login."""
        request = self._request(URL.AUTH_NEW_TOKEN, api_key=tmdb_api_key())
        self._token = self._Token(
            id=request["request_token"], expires_at=request["expires_at"]
        )
        return request

    def _validate_token(self, username, password):
        data = {
            "username": username,
            "password": password,
            "request_token": self._token_id,
        }
        request = self._post_request(
            URL.AUTH_VALIDATE_WITH_LOGIN, data, api_key=tmdb_api_key()
        )
        return request

    @property
    def _session_id(self):
        try:
            return self._session.id
        except AttributeError:
            raise self.SessionError("No session ID. Need to log in.")

    @property
    def _token_id(self):
        try:
            return self._token.id
        except AttributeError:
            raise self.TokenError("No request token ID. Need to log in.")

    @property
    def tmdb_id(self):
        return self._getdata("id")

    @property
    def default_language(self):
        """It is a ISO 639 1 code."""
        return self._getdata("iso_639_1")

    @property
    def fallback_language(self):
        """It is a ISO 3166 1 code."""
        return self._getdata("iso_3166_1")

    @property
    def name(self):
        return self._getdata("name")

    @property
    def username(self):
        return self._getdata("username")

    @property
    def include_adult(self):
        return self._getdata("include_adult")

    def get_details(self):
        """Get your account details."""
        request = self._request(
            URL.ACCOUNT_DETAILS,
            api_key=tmdb_api_key(),
            session_id=self._session_id,
        )
        self.data.update(request)
        return request

    def iter_lists(self, **params):
        """Get lists created by an account. Will include
        private lists if you are the owner."""
        params = {"session_id": self._session_id, **params}
        response = self._iter_request(
            URL.ACCOUNT_CREATED_LISTS.format(account_id=self.tmdb_id), **params
        )
        for item in response:
            yield TMDbList(item["id"], **item)

    def iter_favorite_movies(self, **params):
        """Get your favorite movies."""
        params = {"session_id": self._session_id, **params}
        response = self._iter_request(
            URL.ACCOUNT_FAVORITE_MOVIES.format(account_id=self.tmdb_id),
            **params,
        )
        for item in response:
            yield Movie(item["id"], **item)

    def iter_favorite_shows(self, **params):
        """Get your favorite TV shows."""
        params = {"session_id": self._session_id, **params}
        response = self._iter_request(
            URL.ACCOUNT_FAVORITE_SHOWS.format(account_id=self.tmdb_id),
            **params,
        )
        for item in response:
            yield Show(item["id"], **item)

    def iter_rated_movies(self, **params):
        """Get all the movies you have rated."""
        params = {"session_id": self._session_id, **params}
        response = self._iter_request(
            URL.ACCOUNT_RATED_MOVIES.format(account_id=self.tmdb_id), **params
        )
        for item in response:
            yield Movie(item["id"], **item)

    def iter_rated_shows(self, **params):
        """Get all the TV shows you have rated."""
        params = {"session_id": self._session_id, **params}
        response = self._iter_request(
            URL.ACCOUNT_RATED_SHOWS.format(account_id=self.tmdb_id), **params
        )
        for item in response:
            yield Show(item["id"], **item)

    def iter_rated_episodes(self, **params):
        """Get all the TV episodes you have rated."""
        params = {"session_id": self._session_id, **params}
        response = self._iter_request(
            URL.ACCOUNT_RATED_EPISODES.format(account_id=self.tmdb_id),
            **params,
        )
        for item in response:
            yield Episode(item["id"], **item)

    def iter_movie_watchlist(self, **params):
        """Get all the movies you have added to your watchlist."""
        params = {"session_id": self._session_id, **params}
        response = self._iter_request(
            URL.ACCOUNT_MOVIE_WATCHLIST.format(account_id=self.tmdb_id),
            **params,
        )
        for item in response:
            yield Movie(item["id"], **item)

    def iter_show_watchlist(self, **params):
        """Get all the TV shows you have added to your
        watchlist."""
        params = {"session_id": self._session_id, **params}
        response = self._iter_request(
            URL.ACCOUNT_SHOW_WATCHLIST.format(account_id=self.tmdb_id),
            **params,
        )
        for item in response:
            yield Show(item["id"], **item)

    def mark_as_favorite(self, item):
        """Mark a movie or TV show as a favorite item."""
        if not isinstance(item, (Movie, Show)):
            raise TypeError(
                f"An `item` must be `Movie` or `Show`, not a `{type(item)}`"
            )
        data = {
            "media_type": "movie" if isinstance(item, Movie) else "tv",
            "media_id": item.tmdb_id,
            "favorite": True,
        }
        return self._post_request(
            URL.ACCOUNT_MARK_AS_FAVORITE.format(account_id=self.tmdb_id),
            data,
            session_id=self._session_id,
        )

    def remove_from_favorites(self, item):
        """Remove a movie or TV show from your favorites."""
        if not isinstance(item, (Movie, Show)):
            raise TypeError(
                f"An `item` must be `Movie` or `Show`, not a `{type(item)}`"
            )
        data = {
            "media_type": "movie" if isinstance(item, Movie) else "tv",
            "media_id": item.tmdb_id,
            "favorite": False,
        }
        return self._post_request(
            URL.ACCOUNT_MARK_AS_FAVORITE.format(account_id=self.tmdb_id),
            data,
            session_id=self._session_id,
        )

    def add_to_watchlist(self, item):
        """Add a movie or TV show to your watchlist."""
        if not isinstance(item, (Movie, Show)):
            raise TypeError(
                f"An `item` must be `Movie` or `Show`, not a `{type(item)}`"
            )
        data = {
            "media_type": "movie" if isinstance(item, Movie) else "tv",
            "media_id": item.tmdb_id,
            "watchlist": True,
        }
        return self._post_request(
            URL.ACCOUNT_ADD_TO_WATCHLIST.format(account_id=self.tmdb_id),
            data,
            session_id=self._session_id,
        )

    def remove_from_watchlist(self, item):
        """Add a movie or TV show to your watchlist."""
        if not isinstance(item, (Movie, Show)):
            raise TypeError(
                f"An `item` must be `Movie` or `Show`, not a `{type(item)}`"
            )
        data = {
            "media_type": "movie" if isinstance(item, Movie) else "tv",
            "media_id": item.tmdb_id,
            "watchlist": False,
        }
        return self._post_request(
            URL.ACCOUNT_ADD_TO_WATCHLIST.format(account_id=self.tmdb_id),
            data,
            session_id=self._session_id,
        )

    def rate(self, item, value):
        """Rate a movie, TV show or TV episode. `value` must be
        between `0.5` and `10`"""
        if not isinstance(item, (Movie, Show)):
            raise TypeError(
                f"An `item` must be `Movie` or `Show`, not a `{type(item)}`"
            )
        if not 0.5 <= value <= 10:
            raise TypeError(f"A value must be between 0.5 and 10. Not {value}")
        data = {"value": value}
        if isinstance(item, Movie):
            return self._post_request(
                URL.RATE_MOVIE.format(movie_id=item.tmdb_id),
                data,
                session_id=self._session_id,
            )
        else:
            return self._post_request(
                URL.RATE_SHOW.format(show_id=item.tmdb_id),
                data,
                session_id=self._session_id,
            )

    def delete_rating(self, item):
        """Remove your rating for a movie, TV show or TV
        episode."""
        if not isinstance(item, (Movie, Show)):
            raise TypeError(
                f"An `item` must be `Movie` or `Show`, not a `{type(item)}`"
            )
        if isinstance(item, Movie):
            return self._delete_request(
                URL.DELETE_MOVIE_RATING.format(movie_id=item.tmdb_id),
                {},
                session_id=self._session_id,
            )
        else:
            return self._post_request(
                URL.DELETE_SHOW_RATING.format(show_id=item.tmdb_id),
                {},
                session_id=self._session_id,
            )

    # def create_list(self, name, desc, lang="en"):
    #     """Create a list."""
    #     data = {"name": name, "description": desc, "language": lang}
    #     r = self._post_request(URL.CREATE_LIST, data, session_id=self._session_id)
    #     return TMDbList(r["list_id"], name=name, description=desc, iso_639_1=lang)

    # def delete_list(self, list_): # TODO: raises HTTPError (it is a TMDb problem)
    #     """Delete a list."""
    #     return self._delete_request(
    #         URL.DELETE_LIST.format(list_id=list_.tmdb_id), {}, session_id=self._session_id
    #     )

    # def add_movie_to_list(self, list_, movie):
    #     """Add a movie to a list."""
    #     data = {"media_id": movie.tmdb_id}
    #     r = self._post_request(
    #         URL.ADD_MOVIE_TO_LIST.format(list_id=list_.tmdb_id),
    #         data,
    #         session_id=self._session_id,
    #         confirm=True,
    #     )
    #     if r["status_code"] == 12:
    #         list_._changed = True
    #     return r

    # def remove_movie_from_list(self, list_, movie):
    #     """Remove a movie from a list."""
    #     data = {"media_id": movie.tmdb_id}
    #     r = self._post_request(
    #         URL.REMOVE_MOVIE_FROM_LIST.format(list_id=list_.tmdb_id),
    #         data,
    #         session_id=self._session_id,
    #     )
    #     if r["status_code"] == 13:
    #         list_._changed = True
    #     return r

    # def clear_list(self, list_):
    #     """Clear all of the items from a list."""
    #     r = self._post_request(
    #         URL.CLEAR_LIST.format(list_id=list_.tmdb_id),
    #         None,
    #         session_id=self._session_id,
    #     )
    #     if r["status_code"] == 12:
    #         list_._changed = True
    #     return r


class TMDbList(TMDb):
    """Represents a list."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        _import_all()
        self._changed = False

    def _init(self):
        self.get_details()

    def _getdata(self, key):
        if key not in self.data or self._changed:
            self._init()
            self._changed = False
        return copy.deepcopy(self.data[key])

    @property
    def name(self):
        """The name of a list."""
        return self._getdata("name")

    @property
    def description(self):
        """The description of a list."""
        return self._getdata("description")

    @property
    def creator(self):
        return self._getdata("created_by")

    @property
    def n_favorites(self):
        return self._getdata("favorite_count")

    @property
    def items(self):
        acc = []
        for item in self._getdata("items"):
            if item["media_type"] == "movie":
                Obj = Movie
            elif item["media_type"] == "tv":
                Obj = Show
            acc.append(Obj(item["id"], **item))
        return acc

    @property
    def language(self):
        code = self._getdata("iso_639_1")
        try:
            item = self._all_languages[code]
        except AttributeError:
            self._all_languages = self._get_all_languages()
            item = self._all_languages[code]
        return Language(
            iso_639_1=code,
            english_name=item["english_name"],
            original_name=item["name"],
        )

    def get_details(self, **params):
        details = self._request(
            URL.LIST_DETAILS.format(list_id=self.tmdb_id), **params
        )
        self.n_requests += 1
        self.data.update(details)
        return details

    def has_movie(self, movie):
        r = self._request(
            URL.LIST_CHECK_MOVIE_STATUS.format(list_id=self.tmdb_id),
            movie_id=movie.tmdb_id,
        )
        return r["item_present"]
