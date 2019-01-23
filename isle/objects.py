import copy
from abc import ABC, abstractmethod
from typing import NamedTuple, Iterator, List, Optional, Tuple
from operator import itemgetter

import isle._urls as URL
from isle._config import tmdb_api_key
from isle._requests import DELETE, GET, POST, GET_pages


__all__ = [
    "Account",
    "TMDbList",
    "Movie",
    "Show",
    "Person",
    "Company",
    "Season",
    "Episode",
    "Keyword",
    "Genre",
    "Image",
    "Country",
    "Language",
    "Vote",
    "Video",
    "Credit",
]


def __dir__(name):
    return sorted(__all__)


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

    def __eq__(self, other):
        if other.__class__ is not self.__class__:
            return NotImplemented
        return self.tmdb_id == other.tmdb_id


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


class Company(TMDb):
    """Represents a company."""

    def _init(self):
        self.get_details()

    def _getdata(self, key):
        if key not in self.data:
            if key == "alternative_names":
                self.get_alternative_names()
            elif key == "images":
                self.get_images()
            else:
                self._init()
        return copy.deepcopy(self.data[key])

    @property
    def name(self):
        """Return the name of a company."""
        return self._getdata("name")

    @property
    def also_known_as(self):
        """Return alternative names of a company."""
        names = []
        for item in self._getdata("alternative_names")["results"]:
            names.append(item["name"])
        return names

    @property
    def description(self):
        """Return a company's description."""
        return self._getdata("description")

    @property
    def homepage(self):
        """Return a company's homepage."""
        return self._getdata("homepage")

    @property
    def country(self):
        """Return a company's origin country."""
        code = self._getdata("origin_country")
        if code:
            try:
                english_name = self._all_countries[code]
            except AttributeError:
                self._all_countries = self._get_all_countries()
                english_name = self._all_countries[code]
            return Country(iso_3166_1=code, english_name=english_name)
        else:
            return code

    @property
    def parent_company(self):
        # TODO: definition
        return self._getdata("parent_company")

    @property
    def logos(self):
        """Return logo images that belong to a comapny. Each item
        is an instance of the `Image` class."""
        logos = []
        for item in self._getdata("images")["logos"]:
            logos.append(Image(item, type_="logo"))
        return logos

    def _get_all_countries(self):
        data = self._request(
            URL.COUNTRIES_CONFIGURATION, **{"api_key": tmdb_api_key()}
        )
        countries = {}
        for item in data:
            countries[item["iso_3166_1"]] = item["english_name"]
        return countries

    def get_details(self, **params):
        """Get a companies details."""
        details = self._request(
            URL.COMPANY_DETAILS.format(company_id=self.tmdb_id), **params
        )
        self.data.update(details)
        return details

    def get_alternative_names(self, **params):
        """Get the alternative names of a company."""
        alternative_names = self._request(
            URL.COMPANY_ALTERNATIVE_NAMES.format(company_id=self.tmdb_id),
            **params,
        )
        self.data.update({"alternative_names": alternative_names})
        return alternative_names

    def get_images(self, **params):
        """Get a companies logos."""
        images = self._request(
            URL.COMPANY_IMAGES.format(company_id=self.tmdb_id), **params
        )
        self.data.update({"images": images})
        return images


class Movie(TMDb):
    """Represents a movie."""

    def _init(self):
        return self.get_all()

    @property
    def title(self):
        """Return titles of a movie in different languages.
        Each key is an ISO-3166-1 code (such as `"US"`, `"RU"`,
        etc.), and the value is the corresponding title.

        There is two special keys: `"original"` and `"default"`.
        The first one returns the original movie title and the
        second one depends on the location."""
        titles = {
            "default": self._getdata("title"),
            "original": self._getdata("original_title"),
        }
        for item in self._getdata("translations")["translations"]:
            code, title = item["iso_3166_1"], item["data"]["title"]
            if title:
                titles[code] = title
        return titles

    @property
    def overview(self):
        """Return the overviews of a movie in different
        languages. Each key is an ISO-3166-1 code (such as `"US"`,
        `"RU"`, etc.), and the value is the corresponding overview.

        There is a key `"default"`. It depends on the location."""
        overviews = {"default": self._getdata("overview")}
        for item in self._getdata("translations")["translations"]:
            code, overview = item["iso_3166_1"], item["data"]["overview"]
            if overview:
                overviews[code] = overview
        return overviews

    @property
    def tagline(self):
        """Return a movie slogan"""
        return self._getdata("tagline")

    @property
    def homepage(self):
        """Return a movie homepages. Each key is an ISO-3166-1
        code (such as `"US"`, `"RU"`, etc.) and the value is the
        corresponding homepage.

        There is a key `"default"`. It depends on the location.
        """
        default = self._getdata("homepage")
        pages = {"default": default} if default else {}
        for item in self._getdata("translations")["translations"]:
            code, page = item["iso_3166_1"], item["data"]["homepage"]
            if page:
                pages[code] = page
        return pages

    @property
    def year(self):
        """Return year of a movie."""
        release_date = self._getdata("release_date")
        if release_date:
            return int(release_date[0:4])
        else:
            return None

    @property
    def releases(self):
        """Return release dates of a movie in different
        countries. Each key is an ISO-3166-1 code (such as `"US"`,
        `"RU"`, etc.) and the value is the corresponding date in
        `YYYY-MM-DD` format."""

        def _remove_iso_639_1(d):
            if "iso_639_1" in d:
                del d["iso_639_1"]
            return d

        def _rename_to_date(d):
            if "release_date" in d:
                d["date"] = d["release_date"]
                del d["release_date"]
            return d

        def _default_note(d):
            if "note" not in d:
                d["note"] = ""
            return d

        dates = {}
        for item in self._getdata("release_dates")["results"]:
            release_dates = list(map(_remove_iso_639_1, item["release_dates"]))
            release_dates = list(map(_rename_to_date, release_dates))
            release_dates = list(map(_default_note, release_dates))
            dates[item["iso_3166_1"]] = release_dates
        return dates

    @property
    def is_adult(self):
        """Return `True` if a movie is for adults."""
        return self._getdata("adult")

    @property
    def backdrops(self):
        """Return backdrops that belong to a movie. Each item
        is an instance of the `Image` class."""
        backdrops = []
        for item in self._getdata("images")["backdrops"]:
            backdrops.append(Image(item, type_="backdrop"))
        return backdrops

    @property
    def posters(self):
        """Return posters that belong to a movie. Each item is
        an instance of the `Image` class."""
        posters = []
        for item in self._getdata("images")["posters"]:
            posters.append(Image(item, type_="poster"))
        return posters

    @property
    def languages(self):
        """Return the languages spoken in a movie. Each item is
        an instance of the `Language` class."""
        languages = []
        for code in map(
            itemgetter("iso_639_1"), self._getdata("spoken_languages")
        ):
            try:
                item = self._all_languages[code]
            except AttributeError:
                self._all_languages = self._get_all_languages()
                item = self._all_languages[code]
            languages.append(
                Language(
                    iso_639_1=code,
                    english_name=item["english_name"],
                    original_name=item["name"],
                )
            )
        return languages

    @property
    def countries(self):
        """Return production countries. Each item is an instance of
        the `Country` class."""
        countries = []
        for item in self._getdata("production_countries"):
            countries.append(Country(item["iso_3166_1"], item["name"]))
        return countries

    @property
    def popularity(self):
        """Return popularity of a movie on TMDb.

        See more:
        https://developers.themoviedb.org/3/getting-started/popularity."""
        return self._getdata("popularity")

    @property
    def revenue(self):
        """Return revenue of a movie."""
        return self._getdata("revenue")

    @property
    def budget(self):
        """Return budget of a movie."""
        return self._getdata("budget")

    @property
    def runtime(self):
        """Return a movie runtime."""
        return self._getdata("runtime")

    @property
    def status(self):
        """Return one of this values: `"Rumored"`, `"Planned"`,
        `"In Production"`, `"Post Production"`, `"Released"`,
        `"Canceled"`."""
        return self._getdata("status")

    @property
    def companies(self):
        """Return the production companies. Each item is an
        instance of the `Company` class."""
        companies = []
        for item in self._getdata("production_companies"):
            companies.append(Company(item["id"], **item))
        return companies

    @property
    def cast(self):
        """Return movie cast as list of tuples `(Person, Credit)`."""
        cast = []
        for item in self._getdata("credits")["cast"]:
            kwargs = {
                "credit_type": "cast",
                "media_type": "movie",
                "department": "Acting",
                "job": "Actor",
            }
            credit = Credit(
                item["credit_id"],
                media_data=self.data,
                character=item["character"],
                **kwargs,
            )
            person = Person(item["id"], **item)
            cast.append((person, credit))
        return cast

    @property
    def crew(self):
        """Return movie crew as list of tuples `(Person, Credit)`."""
        crew = []
        for item in self._getdata("credits")["crew"]:
            kwargs = {
                "credit_type": "crew",
                "media_type": "movie",
                "department": item["department"],
                "job": item["job"],
            }
            credit = Credit(item["credit_id"], media_data=self.data, **kwargs)
            person = Person(item["id"], **item)
            crew.append((person, credit))
        return crew

    @property
    def vote(self):
        """Return an instance of the `Vote` class. It is like a
        `NamedTuple` object with two attributes: `average` and
        `count`."""
        average = self._getdata("vote_average")
        count = self._getdata("vote_count")
        return Vote(average=average, count=count)

    @property
    def videos(self):
        """Return videos. Each item is an instance of the `Video`
        class."""
        videos = []
        for item in self._getdata("videos")["results"]:
            url = f"https://www.youtube.com/watch?v={item['key']}"
            videos.append(Video(name=item["name"], type=item["type"], url=url))
        return videos

    @property
    def genres(self):
        """Return a movie genres."""
        genres = []
        for item in self._getdata("genres"):
            genres.append(Genre(tmdb_id=item["id"], name=item["name"]))
        return genres

    @property
    def keywords(self):
        """Return a movie keywords."""
        keywords = []
        for item in self._getdata("keywords")["keywords"]:
            keywords.append(Keyword(item["id"], **item))
        return keywords

    @property
    def imdb_id(self):
        """Return the ID of a movie on IMDb."""
        return self._getdata("external_ids")["imdb_id"]

    @property
    def facebook_id(self):
        """Return the ID of a movie on Facebook."""
        return self._getdata("external_ids")["facebook_id"]

    @property
    def instagram_id(self):
        """Return the ID of a movie on Instagram."""
        return self._getdata("external_ids")["instagram_id"]

    @property
    def twitter_id(self):
        """Return the ID of a movie on Twitter."""
        return self._getdata("external_ids")["twitter_id"]

    def get_all(self, **params):
        """Get all information about a movie. This method
        makes only one API request."""
        methods = ",".join(URL.ALL_MOVIE_SECOND_SUFFIXES)
        all_data = self.get_details(
            **{"append_to_response": methods, **params}
        )
        self.data.update(all_data)
        return all_data

    def get_details(self, **params):
        """Get the primary information about a movie."""
        details = self._request(
            URL.MOVIE_DETAILS.format(movie_id=self.tmdb_id), **params
        )
        self.data.update(details)
        return details

    def get_alternative_titles(self, **params):
        """Get all of the alternative titles for a movie."""
        alternative_titles = self._request(
            URL.MOVIE_ALTERNATIVE_TITLES.format(movie_id=self.tmdb_id),
            **params,
        )
        self.data.update({"alternative_titles": alternative_titles})
        return alternative_titles

    def get_changes(self, **params):
        """Get the changes for a movie. By default only the
        last 24 hours are returned."""
        changes = self._request(
            URL.MOVIE_CHANGES.format(movie_id=self.tmdb_id), **params
        )
        self.data.update({"changes": changes})
        return changes

    def get_credits(self, **params):
        """Get the cast and crew for a movie."""
        credits = self._request(
            URL.MOVIE_CREDITS.format(movie_id=self.tmdb_id), **params
        )
        self.data.update({"credits": credits})
        return credits

    def get_external_ids(self, **params):
        """Get the external ids for a movie. Such as
        Facebook, Instagram, Twitter and IMDb"""
        external_ids = self._request(
            URL.MOVIE_EXTERNAL_IDS.format(movie_id=self.tmdb_id), **params
        )
        self.data.update({"external_ids": external_ids})
        return external_ids

    def get_images(self, **params):
        """Get the images that belong to a movie."""
        images = self._request(
            URL.MOVIE_IMAGES.format(movie_id=self.tmdb_id), **params
        )
        self.data.update({"images": images})
        return images

    def get_keywords(self, **params):
        """Get the keywords that have been added to a movie."""
        keywords = self._request(
            URL.MOVIE_KEYWORDS.format(movie_id=self.tmdb_id), **params
        )
        self.data.update({"keywords": keywords})
        return keywords

    def get_release_dates(self, **params):
        """Get the release date along with the certification
        for a movie."""
        release_dates = self._request(
            URL.MOVIE_RELEASE_DATES.format(movie_id=self.tmdb_id), **params
        )
        self.data.update({"release_dates": release_dates})
        return release_dates

    def get_videos(self, **params):
        """Get the videos that have been added to a movie."""
        videos = self._request(
            URL.MOVIE_VIDEOS.format(movie_id=self.tmdb_id), **params
        )
        self.data.update({"videos": videos})
        return videos

    def get_translations(self, **params):
        """Get a list of translations that have been created
        for a movie."""
        translations = self._request(
            URL.MOVIE_TRANSLATIONS.format(movie_id=self.tmdb_id), **params
        )
        self.data.update({"translations": translations})
        return translations

    def iter_recommendations(self, **params):
        """Get a list of recommended movies for a movie."""
        yield from self._iter_request(
            URL.MOVIE_RECOMMENDATIONS.format(movie_id=self.tmdb_id), **params
        )

    def iter_similar_movies(self, **params):
        """Get a list of recommended movies for a movie."""
        yield from self._iter_request(
            URL.MOVIE_SIMILAR.format(movie_id=self.tmdb_id), **params
        )

    def iter_reviews(self, **params):
        """Get the user reviews for a movie."""
        yield from self._iter_request(
            URL.MOVIE_REVIEWS.format(movie_id=self.tmdb_id), **params
        )

    def iter_lists(self, **params):
        """Get a list of lists that this movie belongs to."""
        yield from self._iter_request(
            URL.MOVIE_LISTS.format(movie_id=self.tmdb_id), **params
        )


class Show(TMDb):
    """Represents a TV show."""

    def _init(self):
        return self.get_all()

    @property
    def title(self):
        """Return titles of a TV show in different languages.
        Each key is an ISO-3166-1 code (such as `"US"`, `"RU"`,
        etc.), and the value is the corresponding title.

        There is two special keys: `"original"` and `"default"`.
        The first one returns the original movie title and the
        second one depends on the location."""
        titles = {
            "default": self._getdata("name"),
            "original": self._getdata("original_name"),
        }
        for item in self._getdata("translations")["translations"]:
            code, title = item["iso_3166_1"], item["data"]["name"]
            if title:
                titles[code] = title
        return titles

    @property
    def overview(self):
        """Return the overviews of a TV show in different
        languages. Each key is an ISO-3166-1 code (such as `"US"`,
        `"RU"`, etc.), and the value is the corresponding overview.

        There is a key `"default"`. It depends on the location."""
        overviews = {"default": self._getdata("overview")}
        for item in self._getdata("translations")["translations"]:
            code, overview = item["iso_3166_1"], item["data"]["overview"]
            if overview:
                overviews[code] = overview
        return overviews

    @property
    def homepage(self):
        """Return a TV show homepages. Each key is an ISO-3166-1
        code (such as `"US"`, `"RU"`, etc.) and the value is the
        corresponding homepage.

        There is a key `"default"`. It depends on the location.
        """
        default = self._getdata("homepage")
        pages = {"default": default} if default else {}
        for item in self._getdata("translations")["translations"]:
            code, page = item["iso_3166_1"], item["data"]["homepage"]
            if page:
                pages[code] = page
        return pages

    @property
    def creators(self):
        """Return the creators of a TV show."""
        creators = []
        for item in self._getdata("created_by"):
            creators.append(Person(item["id"], **item))
        return creators

    @property
    def backdrops(self):
        """Return backdrops that belong to a TV show. Each item
        is an instance of the `Image` class."""
        backdrops = []
        for item in self._getdata("images")["backdrops"]:
            backdrops.append(Image(item, type_="backdrop"))
        return backdrops

    @property
    def posters(self):
        """Return posters that belong to a TV show. Each item is
        an instance of the `Image` class."""
        posters = []
        for item in self._getdata("images")["posters"]:
            posters.append(Image(item, type_="poster"))
        return posters

    @property
    def runtimes(self):
        """Return the running times of TV show episodes."""
        return self._getdata("episode_run_time")

    @property
    def first_air_date(self):
        """Return the air date of the first episode."""
        return self._getdata("first_air_date")

    @property
    def last_air_date(self):
        """Return the air date of the last episode."""
        return self._getdata("last_air_date")

    @property
    def in_production(self):
        """Return `True` if a TV show is in production."""
        return self._getdata("in_production")

    @property
    def languages(self):
        """Return the languages spoken in a TV show. Each item is
        an instance of the `Language` class."""
        iso_codes = self._getdata("languages")
        languages = []
        for code in iso_codes:
            try:
                item = self._all_languages[code]
            except AttributeError:
                self._all_languages = self._get_all_languages()
                item = self._all_languages[code]
            languages.append(
                Language(
                    iso_639_1=code,
                    english_name=item["english_name"],
                    original_name=item["name"],
                )
            )
        return languages

    @property
    def last_episode(self):
        """Return the last episode."""
        item = self._getdata("last_episode_to_air")
        return Episode(
            item["episode_number"],
            show_id=self.tmdb_id,
            season_number=item["season_number"],
        )

    @property
    def next_episode(self):
        """Return the next episode."""
        item = self._getdata("next_episode_to_air")
        if item:
            return Episode(
                item["episode_number"],
                show_id=self.tmdb_id,
                season_number=item["season_number"],
            )
        else:
            return item

    @property
    def n_episodes(self):
        """Return the number of episodes."""
        return self._getdata("number_of_episodes")

    @property
    def n_seasons(self):
        """Return the number of seasons."""
        return self._getdata("number_of_seasons")

    @property
    def countries(self):
        """Return production countries. Each item is an instance of
        the `Country` class."""
        countries = []
        for code in self._getdata("origin_country"):
            if code:
                try:
                    english_name = self._all_countries[code]
                except AttributeError:
                    self._all_countries = self._get_all_countries()
                    english_name = self._all_countries[code]
                countries.append(
                    Country(iso_3166_1=code, english_name=english_name)
                )
            else:
                continue
        return countries

    @property
    def popularity(self):
        """Return popularity of a TV show on TMDb.

        See more:
        https://developers.themoviedb.org/3/getting-started/popularity."""
        return self._getdata("popularity")

    @property
    def companies(self):
        """Return the production companies. Each item is an
        instance of the `Company` class."""
        companies = []
        for item in self._getdata("production_companies"):
            companies.append(Company(item["id"], **item))
        return companies

    @property
    def seasons(self):
        """Return seasons. Each item is an instance of the `Season`
        class."""
        seasons = []
        for item in self._getdata("seasons"):
            seasons.append(
                Season(item["season_number"], show_id=self.tmdb_id, **item)
            )
        return seasons

    @property
    def status(self):
        return self._getdata("status")

    @property
    def type(self):
        return self._getdata("type")

    @property
    def vote(self):
        """Return an instance of the `Vote` class. It is like a
        `NamedTuple` object with two attributes: `average` and
        `count`."""
        average = self._getdata("vote_average")
        count = self._getdata("vote_count")
        return Vote(average=average, count=count)

    @property
    def videos(self):
        """Return videos. Each item is an instance of the `Video`
        class."""
        videos = []
        for item in self._getdata("videos")["results"]:
            url = f"https://www.youtube.com/watch?v={item['key']}"
            videos.append(Video(name=item["name"], type=item["type"], url=url))
        return videos

    @property
    def genres(self):
        """Return a TV show genres."""
        genres = []
        for item in self._getdata("genres"):
            genres.append(Genre(tmdb_id=item["id"], name=item["name"]))
        return genres

    @property
    def keywords(self):
        """Return a TV show keywords."""
        keywords = []
        for item in self._getdata("keywords")["results"]:
            keywords.append(Keyword(item["id"], **item))
        return keywords

    @property
    def imdb_id(self):
        """Return the ID of a TV show on IMDb."""
        return self._getdata("external_ids")["imdb_id"]

    @property
    def tvdb_id(self):
        """Return the ID of a TV show on TVDb."""
        return self._getdata("external_ids")["tvdb_id"]

    @property
    def facebook_id(self):
        """Return the ID of a TV show on Facebook."""
        return self._getdata("external_ids")["facebook_id"]

    @property
    def instagram_id(self):
        """Return the ID of a TV show on Instagram."""
        return self._getdata("external_ids")["instagram_id"]

    @property
    def twitter_id(self):
        """Return the ID of a TV show on Twitter."""
        return self._getdata("external_ids")["twitter_id"]

    @property
    def ratings(self):
        """Return content ratings (certifications) that have been
        added to a TV show. Each key is an ISO-3166-1
        code (such as `"US"`, `"RU"`, etc.) and the value is the
        corresponding rating."""
        ratings = {}
        for item in self._getdata("content_ratings")["results"]:
            ratings[item["iso_3166_1"]] = item["rating"]
        return ratings

    @property
    def cast(self):
        """Return TV show cast as list of tuples
        `(Person, Credit)`."""
        cast = []
        for item in self._getdata("credits")["cast"]:
            kwargs = {
                "credit_type": "cast",
                "media_type": "tv",
                "department": "Acting",
                "job": "Actor",
            }
            credit = Credit(
                item["credit_id"],
                media_data=self.data,
                character=item["character"],
                **kwargs,
            )
            person = Person(item["id"], **item)
            cast.append((person, credit))
        return cast

    @property
    def crew(self):
        """Return TV show crew as list of tuples
        `(Person, Credit)`."""
        crew = []
        for item in self._getdata("credits")["crew"]:
            kwargs = {
                "credit_type": "crew",
                "media_type": "tv",
                "department": item["department"],
                "job": item["job"],
            }
            credit = Credit(item["credit_id"], media_data=self.data, **kwargs)
            person = Person(item["id"], **item)
            crew.append((person, credit))
        return crew

    def _get_all_countries(self):
        data = self._request(
            URL.COUNTRIES_CONFIGURATION, **{"api_key": tmdb_api_key()}
        )
        countries = {}
        for item in data:
            countries[item["iso_3166_1"]] = item["english_name"]
        return countries

    def get_all(self, **params):
        """Get all information about a TV show. This method
        makes only one API request."""
        methods = ",".join(URL.ALL_SHOW_SECOND_SUFFIXES)
        all_data = self.get_details(
            **{"append_to_response": methods, **params}
        )
        self.data.update(all_data)
        return all_data

    def get_details(self, **params):
        """Get the primary information about a TV show."""
        details = self._request(
            URL.SHOW_DETAILS.format(show_id=self.tmdb_id), **params
        )
        self.data.update(details)
        return details

    def get_alternative_titles(self, **params):
        """Get all of the alternative titles for a TV show."""
        alternative_titles = self._request(
            URL.SHOW_ALTERNATIVE_TITLES.format(show_id=self.tmdb_id), **params
        )
        self.data.update({"alternative_titles": alternative_titles})
        return alternative_titles

    def get_changes(self, **params):
        """Get the changes for a TV show. By default only the
        last 24 hours are returned."""
        changes = self._request(
            URL.SHOW_CHANGES.format(show_id=self.tmdb_id), **params
        )
        self.data.update({"changes": changes})
        return changes

    def get_content_ratings(self, **params):
        """Get the list of content ratings (certifications)
        that have been added to a TV show."""
        content_ratings = self._request(
            URL.SHOW_CONTENT_RATINGS.format(show_id=self.tmdb_id), **params
        )
        self.data.update({"content_ratings": content_ratings})
        return content_ratings

    def get_credits(self, **params):
        """Get the cast and crew for a TV show."""
        credits = self._request(
            URL.SHOW_CREDITS.format(show_id=self.tmdb_id), **params
        )
        self.data.update({"credits": credits})
        return credits

    def get_episode_groups(self, **params):
        """Get all of the episode groups that have been
        created for a TV show."""
        episode_groups = self._request(
            URL.SHOW_EPISODE_GROUPS.format(show_id=self.tmdb_id), **params
        )
        self.data.update({"episode_groups": episode_groups})
        return episode_groups

    def get_external_ids(self, **params):
        """Get the external ids for a TV show. Such as
        Facebook, Instagram, Twitter, IMDb and TVDB"""
        external_ids = self._request(
            URL.SHOW_EXTERNAL_IDS.format(show_id=self.tmdb_id), **params
        )
        self.data.update({"external_ids": external_ids})
        return external_ids

    def get_images(self, **params):
        """Get the images that belong to a TV show."""
        images = self._request(
            URL.SHOW_IMAGES.format(show_id=self.tmdb_id), **params
        )
        self.data.update({"images": images})
        return images

    def get_keywords(self, **params):
        """Get the keywords that have been added to a TV show."""
        keywords = self._request(
            URL.SHOW_KEYWORDS.format(show_id=self.tmdb_id), **params
        )
        self.data.update({"keywords": keywords})
        return keywords

    def iter_recommendations(self, **params):
        """Get a list of recommended movies for a TV show."""
        yield from self._iter_request(
            URL.SHOW_RECOMMENDATIONS.format(show_id=self.tmdb_id), **params
        )

    def iter_reviews(self, **params):
        """Get the user reviews for a TV show."""
        yield from self._iter_request(
            URL.SHOW_REVIEWS.format(show_id=self.tmdb_id), **params
        )

    def get_screened_theatrically(self, **params):
        """Get a list of seasons or episodes that have been
        screened in a film festival or theatre."""
        screened_theatrically = self._request(
            URL.SHOW_SCREENED_THEATRICALLY.format(show_id=self.tmdb_id),
            **params,
        )
        self.data.update({"screened_theatrically": screened_theatrically})
        return screened_theatrically

    def iter_similar_shows(self, **params):
        """Get a list of recommended movies for a TV shows."""
        yield from self._iter_request(
            URL.SHOW_SIMILAR.format(show_id=self.tmdb_id), **params
        )

    def get_translations(self, **params):
        """Get a list of the translations that exist for a
        TV show."""
        translations = self._request(
            URL.SHOW_TRANSLATIONS.format(show_id=self.tmdb_id), **params
        )
        self.data.update({"translations": translations})
        return translations

    def get_videos(self, **params):
        """Get the videos that have been added to a TV show."""
        videos = self._request(
            URL.SHOW_VIDEOS.format(show_id=self.tmdb_id), **params
        )
        self.data.update({"videos": videos})
        return videos


class Season(TMDb):
    """Represents a TV show season."""

    def __init__(self, n: int, *, show_id: int, **kwargs):
        self.data = {"season_number": n, **kwargs}
        self.show_id = show_id
        self.number = self.data["season_number"]
        self.n_requests = 0

    def _init(self):
        self.get_all()

    @property
    def tmdb_id(self):
        """Return the ID of a season on TMDb."""
        return self._getdata("id")

    @property
    def n(self):
        """Return a season number."""
        return self._getdata("season_number")

    @property
    def title(self):
        """Return a season's name."""
        return self._getdata("name")

    @property
    def overview(self):
        """Return a season's overview."""
        return self._getdata("overview")

    @property
    def air_date(self):
        """Return the air date of a season."""
        return self._getdata("air_date")

    @property
    def episodes(self):
        """Return a season's episodes."""
        episodes = []
        for item in self._getdata("episodes"):
            episodes.append(
                Episode(
                    item["episode_number"],
                    show_id=self.show_id,
                    season_number=item["season_number"],
                )
            )
        return episodes

    @property
    def tvdb_id(self):
        """Return the ID of a season on TVDb."""
        return self._getdata("external_ids")["tvdb_id"]

    @property
    def posters(self):
        """Return poster images that belong to a season. Each item
        is an instance of the `Image` class."""

        def _i(i):
            return Image(i, type_="poster")

        return list(map(_i, self._getdata("images")["posters"]))

    @property
    def videos(self):
        """Return videos. Each item is an instance of the `Video`
        class."""
        videos = []
        for item in self._getdata("videos")["results"]:
            url = f"https://www.youtube.com/watch?v={item['key']}"
            videos.append(Video(name=item["name"], type=item["type"], url=url))
        return videos

    @property
    def cast(self):
        """Return TV season cast as list of tuples `(Person, Credit)`."""
        cast = []
        for item in self._getdata("credits")["cast"]:
            kwargs = {
                "credit_type": "cast",
                "media_type": "movie",
                "department": "Acting",
                "job": "Actor",
            }
            credit = Credit(
                item["credit_id"],
                media_data=self.data,
                character=item["character"],
                **kwargs,
            )
            person = Person(item["id"], **item)
            cast.append((person, credit))
        return cast

    @property
    def crew(self):
        """Return a TV season crew as list of tuples `(Person, Credit)`."""
        crew = []
        for item in self._getdata("credits")["crew"]:
            kwargs = {
                "credit_type": "crew",
                "media_type": "movie",
                "department": item["department"],
                "job": item["job"],
            }
            credit = Credit(item["credit_id"], media_data=self.data, **kwargs)
            person = Person(item["id"], **item)
            crew.append((person, credit))
        return crew

    def get_all(self, **params):
        """Get all information about a TV season in a single
        response."""
        methods = ",".join(URL.ALL_SEASON_SECOND_SUFFIXES)
        all_data = self.get_details(
            **{"append_to_response": methods, **params}
        )
        self.data.update(all_data)
        return all_data

    def get_details(self, **params):
        """Get the primary TV season details."""
        details = self._request(
            URL.SEASON_DETAILS.format(
                show_id=self.show_id, season_number=self.number
            ),
            **params,
        )
        self.data.update(details)
        return details

    def get_changes(self, **params):
        """Get the changes for a TV season. By default only the
        last 24 hours are returned."""
        changes = self._request(
            URL.SEASON_CHANGES.format(season_id=self.tmdb_id), **params
        )
        self.data.update({"changes": changes})
        return changes

    def get_credits(self, **params):
        """Get the credits for TV season."""
        movie_credits = self._request(
            URL.SEASON_CREDITS.format(
                show_id=self.show_id, season_number=self.number
            ),
            **params,
        )
        self.data.update({"credits": movie_credits})
        return movie_credits

    def get_external_ids(self, **params):
        """Get the external ids for a TV season."""
        external_ids = self._request(
            URL.SEASON_EXTERNAL_IDS.format(
                show_id=self.show_id, season_number=self.number
            ),
            **params,
        )
        self.data.update({"external_ids": external_ids})
        return external_ids

    def get_images(self, **params):
        """Get the images that belong to a TV season."""
        images = self._request(
            URL.SEASON_IMAGES.format(
                show_id=self.show_id, season_number=self.number
            ),
            **params,
        )
        self.data.update({"images": images})
        return images

    def get_videos(self, **params):
        """Get the videos that have been added to a TV season."""
        videos = self._request(
            URL.SEASON_VIDEOS.format(
                show_id=self.show_id, season_number=self.number
            ),
            **params,
        )
        self.data.update({"videos": videos})
        return videos


class Episode(TMDb):
    """Represents a TV show episode."""

    def __init__(self, n, *, show_id, season_number, **kwargs):
        self.data = {
            "episode_number": n,
            "season_number": season_number,
            **kwargs,
        }
        self.show_id = show_id
        self.number = self.data["episode_number"]
        self.season_number = self.data["season_number"]
        self.n_requests = 0

    def _init(self):
        self.get_all()

    @property
    def tmdb_id(self):
        """Return the ID of an episode on TMDb."""
        return self._getdata("id")

    @property
    def tvdb_id(self):
        """Return the ID of an episode on TVDb."""
        return self._getdata("external_ids")["tvdb_id"]

    @property
    def imdb_id(self):
        """Return the ID of an episode on IMDb."""
        return self._getdata("external_ids")["imdb_id"]

    @property
    def air_date(self):
        """Return the air date of an episode."""
        return self._getdata("air_date")

    @property
    def n(self):
        """Return an episode number."""
        return self._getdata("episode_number")

    @property
    def sn(self):
        """Return a season number."""
        return self._getdata("season_number")

    @property
    def title(self):
        """Return titles of an episode in different languages.
        Each key is an ISO-3166-1 code (such as `"US"`, `"RU"`,
        etc.), and the value is the corresponding title.

        There is a key `"default"`. It depends on the location."""

        def _n(n):
            return n["iso_3166_1"], n["data"]["name"]

        names = {}
        names["default"] = self._getdata("name")
        for k, v in map(_n, self._getdata("translations")["translations"]):
            if v:
                names[k] = v
        return names

    @property
    def overview(self):
        """Return the overviews of an episode in different
        languages. Each key is an ISO-3166-1 code (such as `"US"`,
        `"RU"`, etc.), and the value is the corresponding overview.

        There is a key `"default"`. It depends on the location."""

        def _o(o):
            return o["iso_3166_1"], o["data"]["overview"]

        overviews = {}
        overviews["default"] = self._getdata("overview")
        for k, v in map(_o, self._getdata("translations")["translations"]):
            if v:
                overviews[k] = v
        return overviews

    @property
    def stills(self):
        """Return images that belong to an episode. Each item is
        an instance of the `Image` class."""

        def _i(i):
            return Image(i, type_="still")

        return list(map(_i, self._getdata("images")["stills"]))

    @property
    def videos(self):
        """Return videos. Each item is an instance of the `Video`
        class."""
        videos = []
        for item in self._getdata("videos")["results"]:
            url = f"https://www.youtube.com/watch?v={item['key']}"
            videos.append(Video(name=item["name"], type=item["type"], url=url))
        return videos

    @property
    def vote(self):
        """Return an instance of the `Vote` class. It is like a
        `NamedTuple` object with two attributes: `average` and
        `count`."""
        average = self._getdata("vote_average")
        count = self._getdata("vote_average")
        return Vote(average=average, count=count)

    @property
    def cast(self):
        """Return TV episode cast as list of tuples
        `(Person, Credit)`."""
        cast = []
        for item in self._getdata("credits")["cast"]:
            kwargs = {
                "credit_type": "cast",
                "department": "Acting",
                "job": "Actor",
            }
            credit = Credit(
                item["credit_id"],
                media_data=self.data,
                character=item["character"],
                **kwargs,
            )
            person = Person(item["id"], **item)
            cast.append((person, credit))
        return cast

    @property
    def crew(self):
        """Return TV episode crew as list of tuples
        `(Person, Credit)`."""
        crew = []
        for item in self._getdata("credits")["crew"]:
            kwargs = {
                "credit_type": "crew",
                "department": item["department"],
                "job": item["job"],
            }
            credit = Credit(item["credit_id"], media_data=self.data, **kwargs)
            person = Person(item["id"], **item)
            crew.append((person, credit))
        return crew

    @property
    def guest_stars(self):
        """Return TV episode guest stars as list of tuples
        `(Person, Credit)`."""
        guest_stars = []
        for item in self._getdata("credits")["guest_stars"]:
            credit = Credit(
                item["credit_id"],
                media_data=self.data,
                character=item.get("character"),
            )
            person = Person(item["id"], **item)
            guest_stars.append((person, credit))
        return guest_stars

    def get_all(self, **params):
        """Get all information about a TV episode in a single
        response."""
        methods = ",".join(URL.ALL_EPISODE_SECOND_SUFFIXES)
        all_data = self.get_details(
            **{"append_to_response": methods, **params}
        )
        self.data.update(all_data)
        return all_data

    def get_details(self, **params):
        """Get the primary TV episode details."""
        details = self._request(
            URL.EPISODE_DETAILS.format(
                **{
                    "show_id": self.show_id,
                    "season_number": self.season_number,
                    "episode_number": self.number,
                }
            ),
            **params,
        )
        self.data.update(details)
        return details

    def get_changes(self, **params):
        """Get the changes for a TV episode. By default only the
        last 24 hours are returned."""
        changes = self._request(
            URL.EPISODE_CHANGES.format(episode_id=self.tmdb_id), **params
        )
        self.data.update({"changes": changes})
        return changes

    def get_credits(self, **params):
        """Get the credits for TV episode."""
        movie_credits = self._request(
            URL.SEASON_CREDITS.format(
                **{
                    "show_id": self.show_id,
                    "season_number": self.season_number,
                    "episode_number": self.number,
                }
            ),
            **params,
        )
        self.data.update({"credits": movie_credits})
        return movie_credits

    def get_external_ids(self, **params):
        """Get the external ids for a TV episode."""
        external_ids = self._request(
            URL.EPISODE_EXTERNAL_IDS.format(
                **{
                    "show_id": self.show_id,
                    "season_number": self.season_number,
                    "episode_number": self.number,
                }
            ),
            **params,
        )
        self.data.update({"external_ids": external_ids})
        return external_ids

    def get_images(self, **params):
        """Get the images that belong to a TV episode."""
        images = self._request(
            URL.EPISODE_IMAGES.format(
                **{
                    "show_id": self.show_id,
                    "season_number": self.season_number,
                    "episode_number": self.number,
                }
            ),
            **params,
        )
        self.data.update({"images": images})
        return images

    def get_videos(self, **params):
        """Get the videos that have been added to a TV episode."""
        videos = self._request(
            URL.EPISODE_VIDEOS.format(
                **{
                    "show_id": self.show_id,
                    "season_number": self.season_number,
                    "episode_number": self.number,
                }
            ),
            **params,
        )
        self.data.update({"videos": videos})
        return videos

    def get_translations(self, **params):
        """Get a list of the translations that exist for a
        TV episode."""
        translations = self._request(
            URL.EPISODE_TRANSLATIONS.format(
                **{
                    "show_id": self.show_id,
                    "season_number": self.season_number,
                    "episode_number": self.number,
                }
            ),
            **params,
        )
        self.data.update({"translations": translations})
        return translations


class Person(TMDb):
    """Represents a person."""

    def _init(self):
        self.get_all()

    @property
    def name(self):
        """Return the name of the person."""
        return self._getdata("name")

    @property
    def also_known_as(self):
        """Return other names (in other languages)."""
        return self._getdata("also_known_as")

    @property
    def known_for_department(self):
        return self._getdata("known_for_department")

    @property
    def birthday(self):
        """Return date of birth."""
        return self._getdata("birthday")

    @property
    def deathday(self):
        """Return date of birth."""
        return self._getdata("deathday")

    @property
    def gender(self):
        """Return an integer between 0 and 2. Default 0."""
        return self._getdata("gender")

    @property
    def biography(self):
        """Return the biography of a person in different
        languages. Each key is an ISO-3166-1 code (such as `"US"`,
        `"RU"`, etc.), and the value is the corresponding
        biography.

        There is a key `"default"`. It depends on the location."""
        biographies = {"default": self._getdata("biography")}
        for item in self._getdata("translations")["translations"]:
            code, bio = item["iso_3166_1"], item["data"]["biography"]
            if bio:
                biographies[code] = bio
        return biographies

    @property
    def homepage(self):
        """Return a person homepage."""
        self._getdata("homepage")

    @property
    def popularity(self):
        """Return popularity of a person on TMDb.

        See more:
        https://developers.themoviedb.org/3/getting-started/popularity."""
        return self._getdata("popularity")

    @property
    def place_of_birth(self):
        """Return place of birth."""
        return self._getdata("place_of_birth")

    @property
    def is_adult(self):
        return self._getdata("adult")

    @property
    def movie_cast(self):
        """Return movies as list of tuples `(Movie, Credit)`."""
        cast = []
        for item in self._getdata("movie_credits")["cast"]:
            kwargs = {
                "media_type": "movie",
                "credit_type": "cast",
                "department": "Acting",
                "job": "Actor",
            }
            credit = Credit(
                item["credit_id"],
                person_data=self.data,
                character=item["character"],
                **kwargs,
            )
            movie = Movie(item["id"], **item)
            cast.append((movie, credit))
        return cast

    @property
    def movie_crew(self):
        """Return movies as list of tuples `(Movie, Credit)`."""
        crew = []
        for item in self._getdata("movie_credits")["crew"]:
            kwargs = {
                "media_type": "movie",
                "credit_type": "crew",
                "department": item["department"],
                "job": item["job"],
            }
            credit = Credit(item["credit_id"], person_data=self.data, **kwargs)
            movie = Movie(item["id"], **item)
            crew.append((movie, credit))
        return crew

    @property
    def show_cast(self):
        """Return shows as list of tuples `(Show, Credit)`."""
        cast = []
        for item in self._getdata("tv_credits")["cast"]:
            kwargs = {
                "media_type": "tv",
                "credit_type": "cast",
                "department": "Acting",
                "job": "Actor",
            }
            credit = Credit(
                item["credit_id"],
                person_data=self.data,
                character=item["character"],
                **kwargs,
            )
            show = Show(item["id"], **item)
            cast.append((show, credit))
        return cast

    @property
    def show_crew(self):
        """Return shows as list of tuples `(Show, Credit)`."""
        crew = []
        for item in self._getdata("tv_credits")["crew"]:
            kwargs = {
                "media_type": "tv",
                "credit_type": "crew",
                "department": item["department"],
                "job": item["job"],
            }
            credit = Credit(item["credit_id"], person_data=self.data, **kwargs)
            show = Show(item["id"], **item)
            crew.append((show, credit))
        return crew

    @property
    def cast(self):
        """Return movies and shows as list of tuples
        `(Movie or Show, Credit)`."""
        cast = []
        for item in self._getdata("combined_credits")["cast"]:
            kwargs = {
                "media_type": item["media_type"],
                "credit_type": "cast",
                "department": "Acting",
                "job": "Actor",
            }
            credit = Credit(
                item["credit_id"],
                person_data=self.data,
                character=item["character"],
                **kwargs,
            )
            Obj = Show if item["media_type"] == "tv" else Movie
            obj = Obj(item["id"], **item)
            cast.append((obj, credit))
        return cast

    @property
    def crew(self):
        """Return movies and shows as list of tuples
        `(Movie or Show, Credit)`."""
        crew = []
        for item in self._getdata("combined_credits")["crew"]:
            kwargs = {
                "media_type": item["media_type"],
                "credit_type": "cast",
                "department": item["department"],
                "job": item["job"],
            }
            credit = Credit(item["credit_id"], person_data=self.data, **kwargs)
            Obj = Show if item["media_type"] == "tv" else Movie
            obj = Obj(item["id"], **item)
            crew.append((obj, credit))
        return crew

    @property
    def imdb_id(self):
        """Return the ID of a person on IMDb."""
        return self._getdata("external_ids")["imdb_id"]

    @property
    def freebase_mid(self):
        # TODO: definition
        return self._getdata("external_ids")["freebase_mid"]

    @property
    def freebase_id(self):
        # TODO: definition
        return self._getdata("external_ids")["freebase_id"]

    @property
    def tvrage_id(self):
        # TODO: definition
        return self._getdata("external_ids")["tvrage_id"]

    @property
    def facebook_id(self):
        """Return the ID of a person on Facebook."""
        return self._getdata("external_ids")["facebook_id"]

    @property
    def instagram_id(self):
        """Return the ID of a person on Instagram."""
        return self._getdata("external_ids")["instagram_id"]

    @property
    def twitter_id(self):
        """Return the ID of a person on Twitter."""
        return self._getdata("external_ids")["twitter_id"]

    @property
    def profiles(self):
        """Return images that belong to a person. Each item is
        an instance of the `Image` class."""

        def _i(i):
            return Image(i, type_="profile")

        return list(map(_i, self._getdata("images")["profiles"]))

    def get_all(self, **params):
        """Get all information about a person in a single
        response."""
        methods = ",".join(URL.ALL_PERSON_SECOND_SUFFIXES)
        all_data = self.get_details(
            **{"append_to_response": methods, **params}
        )
        self.data.update(all_data)
        return all_data

    def get_details(self, **params):
        """Get the primary person details."""
        details = self._request(
            URL.PERSON_DETAILS.format(person_id=self.tmdb_id), **params
        )
        self.data.update(details)
        return details

    def get_changes(self, **params):
        """Get the changes for a person. By default only the
        last 24 hours are returned."""
        changes = self._request(
            URL.PERSON_CHANGES.format(person_id=self.tmdb_id), **params
        )
        self.data.update({"changes": changes})
        return changes

    def get_movie_credits(self, **params):
        """Get the movie credits for a person."""
        movie_credits = self._request(
            URL.PERSON_MOVIE_CREDITS.format(person_id=self.tmdb_id), **params
        )
        self.data.update({"movie_credits": movie_credits})
        return movie_credits

    def get_show_credits(self, **params):
        """Get the TV show credits for a person."""
        show_credits = self._request(
            URL.PERSON_SHOW_CREDITS.format(person_id=self.tmdb_id), **params
        )
        self.data.update({"tv_credits": show_credits})
        return show_credits

    def get_combined_credits(self, **params):
        """Get the movie and TV credits together in a single
        response."""
        combined_credits = self._request(
            URL.PERSON_COMBINED_CREDITS.format(person_id=self.tmdb_id),
            **params,
        )
        self.data.update({"combined_credits": combined_credits})
        return combined_credits

    def get_external_ids(self, **params):
        """Get the external ids for a person. Such as
        Facebook, Instagram, Twitter and IMDb and others"""
        external_ids = self._request(
            URL.PERSON_EXTERNAL_IDS.format(person_id=self.tmdb_id), **params
        )
        self.data.update({"external_ids": external_ids})
        return external_ids

    def get_images(self, **params):
        """Get the images for a person."""
        images = self._request(
            URL.PERSON_IMAGES.format(person_id=self.tmdb_id), **params
        )
        self.data.update({"images": images})
        return images

    def iter_tagged_images(self, **params):
        """Get the images that this person has been tagged
        in."""
        yield from self._iter_request(
            URL.PERSON_TAGGED_IMAGES.format(person_id=self.tmdb_id), **params
        )

    def get_translations(self, **params):
        """Get a list of translations that have been created
        for a person."""
        translations = self._request(
            URL.PERSON_TRANSLATIONS.format(person_id=self.tmdb_id), **params
        )
        self.data.update({"translations": translations})
        return translations


class Keyword(TMDb):
    """Represents a keyword."""

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
