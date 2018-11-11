import copy
from abc import ABC, abstractmethod
from typing import Iterator, NamedTuple
from datetime import date
from operator import itemgetter
from urllib.parse import urljoin

from ._tools import get_response, search_results_for
from .config import TMDB_API_KEY
from ._urls import (
    BASEURL,
    LANGUAGES_CONFIGURATION_SUFFIX,
    COUNTRIES_CONFIGURATION_SUFFIX,
    MOVIE_DETAILS_SUFFIX,
    MOVIE_ALTERNATIVE_TITLES_SUFFIX,
    MOVIE_CHANGES_SUFFIX,
    MOVIE_CREDITS_SUFFIX,
    MOVIE_EXTERNAL_IDS_SUFFIX,
    MOVIE_IMAGES_SUFFIX,
    MOVIE_KEYWORDS_SUFFIX,
    MOVIE_RELEASE_DATES_SUFFIX,
    MOVIE_VIDEOS_SUFFIX,
    MOVIE_TRANSLATIONS_SUFFIX,
    MOVIE_RECOMMENDATIONS_SUFFIX,
    MOVIE_SIMILAR_SUFFIX,
    MOVIE_REVIEWS_SUFFIX,
    MOVIE_LISTS_SUFFIX,
    ALL_MOVIE_SECOND_SUFFIXES,
    SHOW_DETAILS_SUFFIX,
    SHOW_ALTERNATIVE_TITLES_SUFFIX,
    SHOW_CHANGES_SUFFIX,
    SHOW_CONTENT_RATINGS_SUFFIX,
    SHOW_CREDITS_SUFFIX,
    SHOW_EPISODE_GROUPS_SUFFIX,
    SHOW_EXTERNAL_IDS_SUFFIX,
    SHOW_IMAGES_SUFFIX,
    SHOW_KEYWORDS_SUFFIX,
    SHOW_RECOMMENDATIONS_SUFFIX,
    SHOW_REVIEWS_SUFFIX,
    SHOW_SCREENED_THEATRICALLY_SUFFIX,
    SHOW_SIMILAR_SUFFIX,
    SHOW_TRANSLATIONS_SUFFIX,
    SHOW_VIDEOS_SUFFIX,
    ALL_SHOW_SECOND_SUFFIXES,
    SEASON_DETAILS_SUFFIX,
    SEASON_CHANGES_SUFFIX,
    SEASON_CREDITS_SUFFIX,
    SEASON_EXTERNAL_IDS_SUFFIX,
    SEASON_IMAGES_SUFFIX,
    SEASON_VIDEOS_SUFFIX,
    ALL_SEASON_SECOND_SUFFIXES,
    EPISODE_DETAILS_SUFFIX,
    EPISODE_CHANGES_SUFFIX,
    EPISODE_CREDITS_SUFFIX,
    EPISODE_EXTERNAL_IDS_SUFFIX,
    EPISODE_IMAGES_SUFFIX,
    EPISODE_VIDEOS_SUFFIX,
    EPISODE_TRANSLATIONS_SUFFIX,
    ALL_EPISODE_SECOND_SUFFIXES,
    PERSON_DETAILS_SUFFIX,
    PERSON_CHANGES_SUFFIX,
    PERSON_MOVIE_CREDITS_SUFFIX,
    PERSON_SHOW_CREDITS_SUFFIX,
    PERSON_COMBINED_CREDITS_SUFFIX,
    PERSON_EXTERNAL_IDS_SUFFIX,
    PERSON_IMAGES_SUFFIX,
    PERSON_TAGGED_IMAGES_SUFFIX,
    PERSON_TRANSLATIONS_SUFFIX,
    ALL_PERSON_SECOND_SUFFIXES,
    COMPANY_DETAILS_SUFFIX,
    COMPANY_ALTERNATIVE_NAMES_SUFFIX,
    COMPANY_IMAGES_SUFFIX,
    KEYWORD_DETAILS_SUFFIX,
    KEYWORD_MOVIES_SUFFIX,
)


__all__ = ["Movie", "Show", "Person", "Company", "Keyword", "Genre"]


class TMDb(ABC):
    def __init__(self, tmdb_id: int, **kwargs):
        if not isinstance(tmdb_id, int):
            msg = f"tmdb_id argument must be an integer, not {type(tmdb_id)}"
            raise TypeError(msg)
        self.data = {"id": tmdb_id, **kwargs}
        self.tmdb_id = self.data["id"]

    @abstractmethod
    def _init(self):
        pass

    def _getdata(self, key):
        if key not in self.data:
            self._init()
        return copy.deepcopy(self.data[key])

    def _request(self, url: str, **params) -> dict:
        return get_response(url, **{"api_key": TMDB_API_KEY, **params})

    def _iter_request(self, url: str, **params):
        return search_results_for(url, {"api_key": TMDB_API_KEY, **params})


class Movie(TMDb):
    def _init(self):
        return self.get_all()

    @property
    def title(self):
        def _t(t):
            return t["iso_3166_1"], t["data"]["title"]

        titles = {}
        titles["default"] = self._getdata("title")
        titles["original"] = self._getdata("original_title")
        for k, v in map(_t, self._getdata("translations")["translations"]):
            if v:
                titles[k] = v
        return titles

    @property
    def overview(self):
        def _o(o):
            return o["iso_3166_1"], o["data"]["overview"]

        overviews = {}
        overviews["default"] = self._getdata("overview")
        for k, v in map(_o, self._getdata("translations")["translations"]):
            if v:
                overviews[k] = v
        return overviews

    @property
    def tagline(self):
        return self._getdata("tagline")

    @property
    def homepage(self):
        def _h(h):
            return h["iso_3166_1"], h["data"]["homepage"]

        pages = {}
        if self._getdata("homepage"):
            pages["default"] = self._getdata("homepage")
        for k, v in map(_h, self._getdata("translations")["translations"]):
            if v:
                pages[k] = v
        return pages

    @property
    def year(self):
        release_date = self._getdata("release_date")
        return date.fromisoformat(release_date).year if release_date else None

    @property
    def releases(self):
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
        return self._getdata("adult")

    @property
    def backdrops(self):
        return list(map(Image, self._getdata("images")["backdrops"]))

    @property
    def posters(self):
        return list(map(Image, self._getdata("images")["posters"]))

    @property
    def languages(self):
        languages = []
        for code in map(itemgetter("iso_639_1"), self._getdata("spoken_languages")):
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
        countries = []
        for item in self._getdata("production_countries"):
            countries.append(Country(item["iso_3166_1"], item["name"]))
        return countries

    @property
    def popularity(self):
        return self._getdata("popularity")

    @property
    def revenue(self):
        return self._getdata("revenue")

    @property
    def budget(self):
        return self._getdata("budget")

    @property
    def runtime(self):
        return self._getdata("runtime")

    @property
    def status(self):
        return self._getdata("status")

    @property
    def companies(self):
        def _c(c):
            return Company(c["id"], **c)

        return list(map(_c, self._getdata("production_companies")))

    @property
    def cast(self):
        cast = []
        for item in self._getdata("credits")["cast"]:
            item["person"] = Person(
                item["id"], name=item["name"], gender=item["gender"]
            )
            cast.append(item)
        cast.sort(key=itemgetter("order"))
        return cast

    @property
    def crew(self):
        crew = []
        for item in self._getdata("credits")["crew"]:
            item["person"] = Person(
                item["id"], name=item["name"], gender=item["gender"]
            )
            crew.append(item)
        return crew

    @property
    def vote(self):
        average = self._getdata("vote_average")
        count = self._getdata("vote_count")
        return Vote(average=average, count=count)

    @property
    def videos(self):
        return self._getdata("videos")["results"]

    @property
    def genres(self):
        def _g(g):
            return Genre(tmdb_id=g["id"], name=g["name"])

        return list(map(_g, self._getdata("genres")))

    @property
    def keywords(self):
        def _k(k):
            return Keyword(k["id"], **k)

        return list(map(_k, self._getdata("keywords")["keywords"]))

    @property
    def imdb_id(self):
        return self._getdata("external_ids")["imdb_id"]

    @property
    def facebook_id(self):
        return self._getdata("external_ids")["facebook_id"]

    @property
    def instagram_id(self):
        return self._getdata("external_ids")["instagram_id"]

    @property
    def twitter_id(self):
        return self._getdata("external_ids")["twitter_id"]

    def _get_all_languages(self):
        url = urljoin(BASEURL, LANGUAGES_CONFIGURATION_SUFFIX)
        data = self._request(url, **{"api_key": TMDB_API_KEY})
        languages = {}
        for item in data:
            iso_639_1 = item["iso_639_1"]
            del item["iso_639_1"]
            languages[iso_639_1] = item
        return languages

    def get_all(self, **params):
        """Get all information about a movie. This method
        makes only one API request."""
        methods = ",".join(ALL_MOVIE_SECOND_SUFFIXES)
        all_data = self.get_details(**{"append_to_response": methods, **params})
        self.data.update(all_data)
        return all_data

    def get_details(self, **params) -> dict:
        """Get the primary information about a movie."""
        details = self._request(
            f"{BASEURL}{MOVIE_DETAILS_SUFFIX.format(self.tmdb_id)}", **params
        )
        self.data.update(details)
        return details

    def get_alternative_titles(self, **params) -> dict:
        """Get all of the alternative titles for a movie."""
        alternative_titles = self._request(
            f"{BASEURL}{MOVIE_ALTERNATIVE_TITLES_SUFFIX.format(self.tmdb_id)}", **params
        )
        self.data.update({"alternative_titles": alternative_titles})
        return alternative_titles

    def get_changes(self, **params) -> dict:
        """Get the changes for a movie. By default only the
        last 24 hours are returned."""
        changes = self._request(
            f"{BASEURL}{MOVIE_CHANGES_SUFFIX.format(self.tmdb_id)}", **params
        )
        self.data.update({"changes": changes})
        return changes

    def get_credits(self, **params) -> dict:
        """Get the cast and crew for a movie."""
        credits = self._request(
            f"{BASEURL}{MOVIE_CREDITS_SUFFIX.format(self.tmdb_id)}", **params
        )
        self.data.update({"credits": credits})
        return credits

    def get_external_ids(self, **params) -> dict:
        """Get the external ids for a movie. Such as
        Facebook, Instagram, Twitter and IMDb"""
        external_ids = self._request(
            f"{BASEURL}{MOVIE_EXTERNAL_IDS_SUFFIX.format(self.tmdb_id)}", **params
        )
        self.data.update({"external_ids": external_ids})
        return external_ids

    def get_images(self, **params) -> dict:
        """Get the images that belong to a movie."""
        images = self._request(
            f"{BASEURL}{MOVIE_IMAGES_SUFFIX.format(self.tmdb_id)}", **params
        )
        self.data.update({"images": images})
        return images

    def get_keywords(self, **params) -> dict:
        """Get the keywords that have been added to a movie."""
        keywords = self._request(
            f"{BASEURL}{MOVIE_KEYWORDS_SUFFIX.format(self.tmdb_id)}", **params
        )
        self.data.update({"keywords": keywords})
        return keywords

    def get_release_dates(self, **params) -> dict:
        """Get the release date along with the certification
        for a movie."""
        release_dates = self._request(
            f"{BASEURL}{MOVIE_RELEASE_DATES_SUFFIX.format(self.tmdb_id)}", **params
        )
        self.data.update({"release_dates": release_dates})
        return release_dates

    def get_videos(self, **params) -> dict:
        """Get the videos that have been added to a movie."""
        videos = self._request(
            f"{BASEURL}{MOVIE_VIDEOS_SUFFIX.format(self.tmdb_id)}", **params
        )
        self.data.update({"videos": videos})
        return videos

    def get_translations(self, **params) -> dict:
        """Get a list of translations that have been created
        for a movie."""
        translations = self._request(
            f"{BASEURL}{MOVIE_TRANSLATIONS_SUFFIX.format(self.tmdb_id)}", **params
        )
        self.data.update({"translations": translations})
        return translations

    def iter_recommendations(self, **params) -> Iterator[dict]:
        """Get a list of recommended movies for a movie."""
        yield from self._iter_request(
            f"{BASEURL}{MOVIE_RECOMMENDATIONS_SUFFIX.format(self.tmdb_id)}", **params
        )

    def iter_similar_movies(self, **params) -> Iterator[dict]:
        """Get a list of recommended movies for a movie."""
        yield from self._iter_request(
            f"{BASEURL}{MOVIE_SIMILAR_SUFFIX.format(self.tmdb_id)}", **params
        )

    def iter_reviews(self, **params) -> Iterator[dict]:
        """Get the user reviews for a movie."""
        yield from self._iter_request(
            f"{BASEURL}{MOVIE_REVIEWS_SUFFIX.format(self.tmdb_id)}", **params
        )

    def iter_lists(self, **params) -> Iterator[dict]:
        """Get a list of lists that this movie belongs to."""
        yield from self._iter_request(
            f"{BASEURL}{MOVIE_LISTS_SUFFIX.format(self.tmdb_id)}", **params
        )


class Show(TMDb):
    def _init(self):
        return self.get_all()

    @property
    def name(self):
        def _n(n):
            return n["iso_3166_1"], n["data"]["name"]

        names = {}
        names["default"] = self._getdata("name")
        names["original"] = self._getdata("original_name")
        for k, v in map(_n, self._getdata("translations")["translations"]):
            names[k] = v
        return names

    @property
    def overview(self):
        def _o(o):
            return o["iso_3166_1"], o["data"]["overview"]

        overviews = {}
        overviews["default"] = self._getdata("overview")
        for k, v in map(_o, self._getdata("translations")["translations"]):
            overviews[k] = v
        return overviews

    @property
    def homepage(self):
        def _h(h):
            return h["iso_3166_1"], h["data"]["homepage"]

        pages = {}
        if self._getdata("homepage"):
            pages["default"] = self._getdata("homepage")
        for k, v in map(_h, self._getdata("translations")["translations"]):
            pages[k] = v
        return pages

    @property
    def creators(self):
        def _c(c):
            return Person(c["id"], name=c["name"], gender=c["gender"])

        return [c for c in map(_c, self._getdata("created_by"))]

    @property
    def backdrops(self):
        return list(map(Image, self._getdata("images")["backdrops"]))

    @property
    def posters(self):
        return list(map(Image, self._getdata("images")["posters"]))

    @property
    def runtimes(self):
        return self._getdata("episode_run_time")

    @property
    def first_air_date(self):
        return self._getdata("first_air_date")

    @property
    def last_air_date(self):
        return self._getdata("last_air_date")

    @property
    def in_production(self):
        return self._getdata("in_production")

    @property
    def languages(self):
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
        item = self._getdata("last_episode_to_air")
        return Episode(
            item["episode_number"],
            show_id=self.tmdb_id,
            season_number=item["season_number"],
        )

    @property
    def next_episode(self):
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
        return self._getdata("number_of_episodes")

    @property
    def n_seasons(self):
        return self._getdata("number_of_seasons")

    @property
    def countries(self):
        countries = []
        for code in self._getdata("origin_country"):
            try:
                english_name = self._all_countries[code]
            except AttributeError:
                self._all_countries = self._get_all_countries()
                english_name = self._all_countries[code]
            countries.append(Country(iso_3166_1=code, english_name=english_name))
        return countries

    @property
    def popularity(self):
        return self._getdata("popularity")

    @property
    def companies(self):
        def _c(c):
            return Company(c["id"], **c)

        return list(map(_c, self._getdata("production_companies")))

    @property
    def seasons(self):
        seasons = []
        for item in self._getdata("seasons"):
            seasons.append(Season(item["season_number"], show_id=self.tmdb_id, **item))
        return seasons

    @property
    def status(self):
        return self._getdata("status")

    @property
    def type(self):
        return self._getdata("type")

    @property
    def vote(self):
        average = self._getdata("vote_average")
        count = self._getdata("vote_count")
        return Vote(average=average, count=count)

    @property
    def videos(self):
        return self._getdata("videos")["results"]

    @property
    def genres(self):
        def _g(g):
            return Genre(tmdb_id=g["id"], name=g["name"])

        return list(map(_g, self._getdata("genres")))

    @property
    def keywords(self):
        def _k(k):
            return Keyword(k["id"], **k)

        return list(map(_k, self._getdata("keywords")["results"]))

    @property
    def imdb_id(self):
        return self._getdata("external_ids")["imdb_id"]

    @property
    def tvdb_id(self):
        return self._getdata("external_ids")["tvdb_id"]

    @property
    def facebook_id(self):
        return self._getdata("external_ids")["facebook_id"]

    @property
    def instagram_id(self):
        return self._getdata("external_ids")["instagram_id"]

    @property
    def twitter_id(self):
        return self._getdata("external_ids")["twitter_id"]

    @property
    def ratings(self):
        ratings = {}
        for item in self._getdata("content_ratings")["results"]:
            ratings[item["iso_3166_1"]] = item["rating"]
        return ratings

    @property
    def cast(self):
        cast = []
        for item in self._getdata("credits")["cast"]:
            item["person"] = Person(
                item["id"], name=item["name"], gender=item["gender"]
            )
            cast.append(item)
        cast.sort(key=itemgetter("order"))
        return cast

    @property
    def crew(self):
        crew = []
        for item in self._getdata("credits")["crew"]:
            item["person"] = Person(
                item["id"], name=item["name"], gender=item["gender"]
            )
            crew.append(item)
        return crew

    def _get_all_languages(self):
        url = urljoin(BASEURL, LANGUAGES_CONFIGURATION_SUFFIX)
        data = self._request(url, **{"api_key": TMDB_API_KEY})
        languages = {}
        for item in data:
            iso_639_1 = item["iso_639_1"]
            del item["iso_639_1"]
            languages[iso_639_1] = item
        return languages

    def _get_all_countries(self):
        url = urljoin(BASEURL, COUNTRIES_CONFIGURATION_SUFFIX)
        data = self._request(url, **{"api_key": TMDB_API_KEY})
        countries = {}
        for item in data:
            countries[item["iso_3166_1"]] = item["english_name"]
        return countries

    def get_all(self, **params):
        """Get all information about a TV show. This method
        makes only one API request."""
        methods = ",".join(ALL_SHOW_SECOND_SUFFIXES)
        all_data = self.get_details(**{"append_to_response": methods, **params})
        self.data.update(all_data)
        return all_data

    def get_details(self, **params) -> dict:
        """Get the primary information about a TV show."""
        details = self._request(
            f"{BASEURL}{SHOW_DETAILS_SUFFIX.format(self.tmdb_id)}", **params
        )
        self.data.update(details)
        return details

    def get_alternative_titles(self, **params) -> dict:
        """Get all of the alternative titles for a TV show."""
        alternative_titles = self._request(
            f"{BASEURL}{SHOW_ALTERNATIVE_TITLES_SUFFIX.format(self.tmdb_id)}", **params
        )
        self.data.update({"alternative_titles": alternative_titles})
        return alternative_titles

    def get_changes(self, **params) -> dict:
        """Get the changes for a TV show. By default only the
        last 24 hours are returned."""
        changes = self._request(
            f"{BASEURL}{SHOW_CHANGES_SUFFIX.format(self.tmdb_id)}", **params
        )
        self.data.update({"changes": changes})
        return changes

    def get_content_ratings(self, **params) -> dict:
        """Get the list of content ratings (certifications)
        that have been added to a TV show."""
        content_ratings = self._request(
            f"{BASEURL}{SHOW_CONTENT_RATINGS_SUFFIX.format(self.tmdb_id)}", **params
        )
        self.data.update({"content_ratings": content_ratings})
        return content_ratings

    def get_credits(self, **params) -> dict:
        """Get the cast and crew for a TV show."""
        credits = self._request(
            f"{BASEURL}{SHOW_CREDITS_SUFFIX.format(self.tmdb_id)}", **params
        )
        self.data.update({"credits": credits})
        return credits

    def get_episode_groups(self, **params):
        """Get all of the episode groups that have been
        created for a TV show."""
        episode_groups = self._request(
            f"{BASEURL}{SHOW_EPISODE_GROUPS_SUFFIX.format(self.tmdb_id)}", **params
        )
        self.data.update({"episode_groups": episode_groups})
        return episode_groups

    def get_external_ids(self, **params) -> dict:
        """Get the external ids for a TV show. Such as
        Facebook, Instagram, Twitter, IMDb and TVDB"""
        external_ids = self._request(
            f"{BASEURL}{SHOW_EXTERNAL_IDS_SUFFIX.format(self.tmdb_id)}", **params
        )
        self.data.update({"external_ids": external_ids})
        return external_ids

    def get_images(self, **params) -> dict:
        """Get the images that belong to a TV show."""
        images = self._request(
            f"{BASEURL}{SHOW_IMAGES_SUFFIX.format(self.tmdb_id)}", **params
        )
        self.data.update({"images": images})
        return images

    def get_keywords(self, **params) -> dict:
        """Get the keywords that have been added to a TV show."""
        keywords = self._request(
            f"{BASEURL}{SHOW_KEYWORDS_SUFFIX.format(self.tmdb_id)}", **params
        )
        self.data.update({"keywords": keywords})
        return keywords

    def iter_recommendations(self, **params) -> Iterator[dict]:
        """Get a list of recommended movies for a TV show."""
        yield from self._iter_request(
            f"{BASEURL}{SHOW_RECOMMENDATIONS_SUFFIX.format(self.tmdb_id)}", **params
        )

    def iter_reviews(self, **params) -> Iterator[dict]:
        """Get the user reviews for a TV show."""
        yield from self._iter_request(
            f"{BASEURL}{SHOW_REVIEWS_SUFFIX.format(self.tmdb_id)}", **params
        )

    def get_screened_theatrically(self, **params):
        """Get a list of seasons or episodes that have been
        screened in a film festival or theatre."""
        screened_theatrically = self._request(
            f"{BASEURL}{SHOW_SCREENED_THEATRICALLY_SUFFIX.format(self.tmdb_id)}",
            **params,
        )
        self.data.update({"screened_theatrically": screened_theatrically})
        return screened_theatrically

    def iter_similar_shows(self, **params) -> Iterator[dict]:
        """Get a list of recommended movies for a TV shows."""
        yield from self._iter_request(
            f"{BASEURL}{SHOW_SIMILAR_SUFFIX.format(self.tmdb_id)}", **params
        )

    def get_translations(self, **params) -> dict:
        """Get a list of the translations that exist for a
        TV show."""
        translations = self._request(
            f"{BASEURL}{SHOW_TRANSLATIONS_SUFFIX.format(self.tmdb_id)}", **params
        )
        self.data.update({"translations": translations})
        return translations

    def get_videos(self, **params) -> dict:
        """Get the videos that have been added to a TV show."""
        videos = self._request(
            f"{BASEURL}{SHOW_VIDEOS_SUFFIX.format(self.tmdb_id)}", **params
        )
        self.data.update({"videos": videos})
        return videos


class Person(TMDb):
    def _init(self):
        self.get_all()

    @property
    def name(self):
        return self._getdata("name")

    @property
    def also_known_as(self):
        return self._getdata("also_known_as")

    @property
    def known_for_department(self):
        return self._getdata("known_for_department")

    @property
    def birthday(self):
        return self._getdata("birthday")

    @property
    def deathday(self):
        return self._getdata("deathday")

    @property
    def gender(self):
        return self._getdata("gender")

    @property
    def biography(self):
        def _b(b):
            return b["iso_3166_1"], b["data"]["biography"]

        biographies = {}
        biographies["default"] = self._getdata("biography")
        for k, v in map(_b, self._getdata("translations")["translations"]):
            biographies[k] = v
        return biographies

    @property
    def homepage(self):
        self._getdata("homepage")

    @property
    def popularity(self):
        return self._getdata("popularity")

    @property
    def place_of_birth(self):
        return self._getdata("place_of_birth")

    @property
    def is_adult(self):
        return self._getdata("adult")

    @property
    def movie_cast(self):
        cast = []
        for item in self._getdata("movie_credits")["cast"]:
            cast.append(
                {
                    "character": item["character"],
                    "credit_id": item["credit_id"],
                    "movie": Movie(item["id"], **item),
                }
            )
        return cast

    @property
    def movie_crew(self):
        crew = []
        for item in self._getdata("movie_credits")["crew"]:
            crew.append(
                {
                    "department": item["department"],
                    "job": item["job"],
                    "credit_id": item["credit_id"],
                    "movie": Movie(item["id"], **item),
                }
            )
        return crew

    @property
    def show_cast(self):
        cast = []
        for item in self._getdata("tv_credits")["cast"]:
            cast.append(
                {
                    "character": item["character"],
                    "credit_id": item["credit_id"],
                    "show": Show(item["id"], **item),
                }
            )
        return cast

    @property
    def show_crew(self):
        crew = []
        for item in self._getdata("tv_credits")["crew"]:
            crew.append(
                {
                    "department": item["department"],
                    "job": item["job"],
                    "credit_id": item["credit_id"],
                    "show": Show(item["id"], **item),
                }
            )
        return crew

    @property
    def cast(self):
        cast = []
        for item in self._getdata("combined_credits")["cast"]:
            if item["media_type"] == "tv":
                obj = Show(item["id"], **item)
                key = "show"
            else:
                obj = Movie(item["id"], **item)
                key = "movie"
            cast.append(
                {
                    "character": item["character"],
                    "credit_id": item["credit_id"],
                    "media_type": item["media_type"],
                    key: obj,
                }
            )
        return cast

    @property
    def crew(self):
        crew = []
        for item in self._getdata("combined_credits")["crew"]:
            if item["media_type"] == "tv":
                obj = Show(item["id"], **item)
                key = "show"
            else:
                obj = Movie(item["id"], **item)
                key = "movie"
            crew.append(
                {
                    "department": item["department"],
                    "job": item["job"],
                    "credit_id": item["credit_id"],
                    "media_type": item["media_type"],
                    key: obj,
                }
            )
        return crew

    @property
    def imdb_id(self):
        return self._getdata("external_ids")["imdb_id"]

    @property
    def freebase_mid(self):
        return self._getdata("external_ids")["freebase_mid"]

    @property
    def freebase_id(self):
        return self._getdata("external_ids")["freebase_id"]

    @property
    def tvrage_id(self):
        return self._getdata("external_ids")["tvrage_id"]

    @property
    def facebook_id(self):
        return self._getdata("external_ids")["facebook_id"]

    @property
    def instagram_id(self):
        return self._getdata("external_ids")["instagram_id"]

    @property
    def twitter_id(self):
        return self._getdata("external_ids")["twitter_id"]

    @property
    def profiles(self):
        return list(map(Image, self._getdata("images")["profiles"]))

    def get_all(self, **params):
        """Get all information about a person in a single
        response."""
        methods = ",".join(ALL_PERSON_SECOND_SUFFIXES)
        all_data = self.get_details(**{"append_to_response": methods, **params})
        self.data.update(all_data)
        return all_data

    def get_details(self, **params) -> dict:
        """Get the primary person details."""
        details = self._request(
            f"{BASEURL}{PERSON_DETAILS_SUFFIX.format(self.tmdb_id)}", **params
        )
        self.data.update(details)
        return details

    def get_changes(self, **params) -> dict:
        """Get the changes for a person. By default only the
        last 24 hours are returned."""
        changes = self._request(
            f"{BASEURL}{PERSON_CHANGES_SUFFIX.format(self.tmdb_id)}", **params
        )
        self.data.update({"changes": changes})
        return changes

    def get_movie_credits(self, **params) -> dict:
        """Get the movie credits for a person."""
        movie_credits = self._request(
            f"{BASEURL}{PERSON_MOVIE_CREDITS_SUFFIX.format(self.tmdb_id)}", **params
        )
        self.data.update({"movie_credits": movie_credits})
        return movie_credits

    def get_show_credits(self, **params) -> dict:
        """Get the TV show credits for a person."""
        show_credits = self._request(
            f"{BASEURL}{PERSON_SHOW_CREDITS_SUFFIX.format(self.tmdb_id)}", **params
        )
        self.data.update({"tv_credits": show_credits})
        return show_credits

    def get_combined_credits(self, **params) -> dict:
        """Get the movie and TV credits together in a single
        response."""
        combined_credits = self._request(
            f"{BASEURL}{PERSON_COMBINED_CREDITS_SUFFIX.format(self.tmdb_id)}", **params
        )
        self.data.update({"combined_credits": combined_credits})
        return combined_credits

    def get_external_ids(self, **params) -> dict:
        """Get the external ids for a person. Such as
        Facebook, Instagram, Twitter and IMDb and others"""
        external_ids = self._request(
            f"{BASEURL}{PERSON_EXTERNAL_IDS_SUFFIX.format(self.tmdb_id)}", **params
        )
        self.data.update({"external_ids": external_ids})
        return external_ids

    def get_images(self, **params) -> dict:
        """Get the images for a person."""
        images = self._request(
            f"{BASEURL}{PERSON_IMAGES_SUFFIX.format(self.tmdb_id)}", **params
        )
        self.data.update({"images": images})
        return images

    def iter_tagged_images(self, **params) -> Iterator[dict]:
        """Get the images that this person has been tagged
        in."""
        yield from self._iter_request(
            f"{BASEURL}{PERSON_TAGGED_IMAGES_SUFFIX.format(self.tmdb_id)}", **params
        )

    def get_translations(self, **params) -> dict:
        """Get a list of translations that have been created
        for a person."""
        translations = self._request(
            f"{BASEURL}{PERSON_TRANSLATIONS_SUFFIX.format(self.tmdb_id)}", **params
        )
        self.data.update({"translations": translations})
        return translations


class Company(TMDb):
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
        return self._getdata("name")

    @property
    def also_known_as(self):
        names = []
        for item in self._getdata("alternative_names")["results"]:
            names.append(item["name"])
        return names

    @property
    def description(self):
        return self._getdata("description")

    @property
    def homepage(self):
        return self._getdata("homepage")

    @property
    def country(self):
        code = self._getdata("origin_country")
        try:
            english_name = self._all_countries[code]
        except AttributeError:
            self._all_countries = self._get_all_countries()
            english_name = self._all_countries[code]
        return Country(iso_3166_1=code, english_name=english_name)

    @property
    def parent_company(self):
        return self._getdata("parent_company")

    @property
    def logos(self):
        return list(map(Image, self._getdata("images")["logos"]))

    def _get_all_countries(self):
        url = urljoin(BASEURL, COUNTRIES_CONFIGURATION_SUFFIX)
        data = self._request(url, **{"api_key": TMDB_API_KEY})
        countries = {}
        for item in data:
            countries[item["iso_3166_1"]] = item["english_name"]
        return countries

    def get_details(self, **params) -> dict:
        """Get a companies details."""
        details = self._request(
            f"{BASEURL}{COMPANY_DETAILS_SUFFIX.format(self.tmdb_id)}", **params
        )
        self.data.update(details)
        return details

    def get_alternative_names(self, **params) -> dict:
        """Get the alternative names of a company."""
        alternative_names = self._request(
            f"{BASEURL}{COMPANY_ALTERNATIVE_NAMES_SUFFIX.format(self.tmdb_id)}",
            **params,
        )
        self.data.update({"alternative_names": alternative_names})
        return alternative_names

    def get_images(self, **params) -> dict:
        """Get a companies logos."""
        images = self._request(
            f"{BASEURL}{COMPANY_IMAGES_SUFFIX.format(self.tmdb_id)}", **params
        )
        self.data.update({"images": images})
        return images


class Keyword(TMDb):
    def _init(self):
        self.get_details()

    @property
    def name(self):
        return self._getdata("name")

    def get_details(self) -> dict:
        """Get the primary information about a keyword."""
        details = self._request(
            f"{BASEURL}{KEYWORD_DETAILS_SUFFIX.format(self.tmdb_id)}", **{}
        )
        self.data.update(details)
        return details

    def iter_movies(self, **params) -> Iterator[Movie]:
        """Get the movies that belong to a keyword."""
        results = self._iter_request(
            f"{BASEURL}{KEYWORD_MOVIES_SUFFIX.format(self.tmdb_id)}", **params
        )
        yield from map(lambda x: Movie(x["id"]), results)

    def __str__(self):
        return self._getdata("name")


class Season(TMDb):
    def __init__(self, n, *, show_id, **kwargs):
        self.data = {"season_number": n, **kwargs}
        self.show_id = show_id
        self.number = self.data["season_number"]

    def _init(self):
        self.get_all()

    @property
    def tmdb_id(self):
        return self._getdata("id")

    @property
    def n(self):
        return self._getdata("season_number")

    @property
    def name(self):
        return self._getdata("name")

    @property
    def overview(self):
        return self._getdata("overview")

    @property
    def air_date(self):
        return self._getdata("air_date")

    @property
    def episodes(self):
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
        return self._getdata("external_ids")["tvdb_id"]

    @property
    def posters(self):
        return list(map(Image, self._getdata("images")["posters"]))

    @property
    def videos(self):
        return self._getdata("videos")["results"]

    @property
    def cast(self):
        cast = []
        for item in self._getdata("credits")["cast"]:
            item["person"] = Person(
                item["id"], name=item["name"], gender=item["gender"]
            )
            cast.append(item)
        cast.sort(key=itemgetter("order"))
        return cast

    @property
    def crew(self):
        crew = []
        for item in self._getdata("credits")["crew"]:
            item["person"] = Person(
                item["id"], name=item["name"], gender=item["gender"]
            )
            crew.append(item)
        return crew

    def get_all(self, **params):
        """Get all information about a TV season in a single
        response."""
        methods = ",".join(ALL_SEASON_SECOND_SUFFIXES)
        all_data = self.get_details(**{"append_to_response": methods, **params})
        self.data.update(all_data)
        return all_data

    def get_details(self, **params) -> dict:
        """Get the primary TV season details."""
        details = self._request(
            f"{BASEURL}{SEASON_DETAILS_SUFFIX.format(self.show_id, self.number)}",
            **params,
        )
        self.data.update(details)
        return details

    def get_changes(self, **params) -> dict:
        """Get the changes for a TV season. By default only the
        last 24 hours are returned."""
        changes = self._request(
            f"{BASEURL}{SEASON_CHANGES_SUFFIX.format(self.tmdb_id)}", **params
        )
        self.data.update({"changes": changes})
        return changes

    def get_credits(self, **params) -> dict:
        """Get the credits for TV season."""
        movie_credits = self._request(
            f"{BASEURL}{SEASON_CREDITS_SUFFIX.format(self.show_id, self.number)}",
            **params,
        )
        self.data.update({"credits": movie_credits})
        return movie_credits

    def get_external_ids(self, **params) -> dict:
        """Get the external ids for a TV season."""
        external_ids = self._request(
            f"{BASEURL}{SEASON_EXTERNAL_IDS_SUFFIX.format(self.show_id, self.number)}",
            **params,
        )
        self.data.update({"external_ids": external_ids})
        return external_ids

    def get_images(self, **params) -> dict:
        """Get the images that belong to a TV season."""
        images = self._request(
            f"{BASEURL}{SEASON_IMAGES_SUFFIX.format(self.show_id, self.number)}",
            **params,
        )
        self.data.update({"images": images})
        return images

    def get_videos(self, **params) -> dict:
        """Get the videos that have been added to a TV season."""
        videos = self._request(
            f"{BASEURL}{SEASON_VIDEOS_SUFFIX.format(self.show_id, self.number)}",
            **params,
        )
        self.data.update({"videos": videos})
        return videos


class Episode(TMDb):
    def __init__(self, n, *, show_id, season_number, **kwargs):
        self.data = {"episode_number": n, "season_number": season_number}
        self.show_id = show_id
        self.number = self.data["episode_number"]
        self.season_number = self.data["season_number"]

    def _init(self):
        self.get_all()

    @property
    def tmdb_id(self):
        return self._getdata("id")

    @property
    def tvdb_id(self):
        return self._getdata("external_ids")["tvdb_id"]

    @property
    def imdb_id(self):
        return self._getdata("external_ids")["imdb_id"]

    @property
    def air_date(self):
        return self._getdata("air_date")

    @property
    def n(self):
        return self._getdata("episode_number")

    @property
    def sn(self):
        return self._getdata("season_number")

    @property
    def name(self):
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
        return list(map(Image, self._getdata("images")["stills"]))

    @property
    def videos(self):
        return self._getdata("videos")["results"]

    @property
    def vote(self):
        average = self._getdata("vote_average")
        count = self._getdata("vote_average")
        return Vote(average=average, count=count)

    @property
    def cast(self):
        cast = []
        for item in self._getdata("credits")["cast"]:
            item["person"] = Person(item["id"], **item)
            cast.append(item)
        cast.sort(key=itemgetter("order"))
        return cast

    @property
    def crew(self):
        crew = []
        for item in self._getdata("credits")["crew"]:
            item["person"] = Person(item["id"], **item)
            crew.append(item)
        return crew

    @property
    def guest_stars(self):
        guest_stars = []
        for item in self._getdata("credits")["guest_stars"]:
            item["person"] = Person(item["id"], **item)
            guest_stars.append(item)
        return guest_stars

    def get_all(self, **params):
        """Get all information about a TV episode in a single
        response."""
        methods = ",".join(ALL_EPISODE_SECOND_SUFFIXES)
        all_data = self.get_details(**{"append_to_response": methods, **params})
        self.data.update(all_data)
        return all_data

    def get_details(self, **params) -> dict:
        """Get the primary TV episode details."""
        details = self._request(
            f"{BASEURL}{EPISODE_DETAILS_SUFFIX.format(self.show_id, self.season_number, self.number)}",
            **params,
        )
        self.data.update(details)
        return details

    def get_changes(self, **params) -> dict:
        """Get the changes for a TV episode. By default only the
        last 24 hours are returned."""
        changes = self._request(
            f"{BASEURL}{EPISODE_CHANGES_SUFFIX.format(self.tmdb_id)}", **params
        )
        self.data.update({"changes": changes})
        return changes

    def get_credits(self, **params) -> dict:
        """Get the credits for TV episode."""
        movie_credits = self._request(
            f"{BASEURL}{SEASON_CREDITS_SUFFIX.format(self.show_id, self.season_number, self.number)}",
            **params,
        )
        self.data.update({"credits": movie_credits})
        return movie_credits

    def get_external_ids(self, **params) -> dict:
        """Get the external ids for a TV episode."""
        external_ids = self._request(
            f"{BASEURL}{EPISODE_EXTERNAL_IDS_SUFFIX.format(self.show_id, self.season_number, self.number)}",
            **params,
        )
        self.data.update({"external_ids": external_ids})
        return external_ids

    def get_images(self, **params) -> dict:
        """Get the images that belong to a TV episode."""
        images = self._request(
            f"{BASEURL}{EPISODE_IMAGES_SUFFIX.format(self.show_id, self.season_number, self.number)}",
            **params,
        )
        self.data.update({"images": images})
        return images

    def get_videos(self, **params) -> dict:
        """Get the videos that have been added to a TV episode."""
        videos = self._request(
            f"{BASEURL}{EPISODE_VIDEOS_SUFFIX.format(self.show_id, self.season_number, self.number)}",
            **params,
        )
        self.data.update({"videos": videos})
        return videos

    def get_translations(self, **params) -> dict:
        """Get a list of the translations that exist for a
        TV episode."""
        translations = self._request(
            f"{BASEURL}{EPISODE_TRANSLATIONS_SUFFIX.format(self.show_id, self.season_number, self.number)}",
            **params,
        )
        self.data.update({"translations": translations})
        return translations


class Genre(NamedTuple):
    tmdb_id: str
    name: str

    def __str__(self):
        return self.name


class Image:
    def __init__(self, image: dict):
        for key, value in image.items():
            setattr(self, key, value)


class Country(NamedTuple):
    iso_3166_1: str
    english_name: str

    def __str__(self):
        return self.english_name


class Language(NamedTuple):
    iso_639_1: str
    english_name: str
    original_name: str

    def __str__(self):
        return self.english_name


class Vote(NamedTuple):
    average: float
    count: str

    def __str__(self):
        return self.average
