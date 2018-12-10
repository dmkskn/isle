from __future__ import annotations

from datetime import date
from operator import itemgetter
from typing import Iterator, List, Optional, Tuple

import themoviedb._urls as URL
import themoviedb.objects._tmdb as _tmdb_objs
import themoviedb.objects.company as company_obj
import themoviedb.objects.others as other_objs
import themoviedb.objects.person as person_obj


class Movie(_tmdb_objs.TMDb):
    """Represents a movie."""

    def _init(self):
        return self.get_all()

    @property
    def title(self) -> dict:
        """Return titles of a movie in different languages.
        Each key is an ISO-3166-1 code (such as `"US"`, `"RU"`,
        etc.), and the value is the corresponding title.

        There is two special keys: `"original"` and `"default"`.
        The first one returns the original movie title and the
        second one depends on the location."""

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
    def overview(self) -> dict:
        """Return the overviews of a movie in different
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
    def tagline(self) -> Optional[str]:
        """Return a movie slogan"""
        return self._getdata("tagline")

    @property
    def homepage(self) -> dict:
        """Return a movie homepages. Each key is an ISO-3166-1
        code (such as `"US"`, `"RU"`, etc.) and the value is the
        corresponding homepage.

        There is a key `"default"`. It depends on the location.
        """

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
    def year(self) -> Optional[int]:
        """Return year of a movie."""
        release_date = self._getdata("release_date")
        return date.fromisoformat(release_date).year if release_date else None

    @property
    def releases(self) -> dict:
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
    def is_adult(self) -> bool:
        """Return `True` if a movie is for adults."""
        return self._getdata("adult")

    @property
    def backdrops(self) -> List[other_objs.Image]:
        """Return backdrops that belong to a movie. Each item
        is an instance of the `Image` class."""

        def _i(i):
            return other_objs.Image(i, type_="backdrop")

        return list(map(_i, self._getdata("images")["backdrops"]))

    @property
    def posters(self) -> List[other_objs.Image]:
        """Return posters that belong to a movie. Each item is
        an instance of the `Image` class."""

        def _i(i):
            return other_objs.Image(i, type_="poster")

        return list(map(_i, self._getdata("images")["posters"]))

    @property
    def languages(self) -> List[other_objs.Language]:
        """Return the languages spoken in a movie. Each item is
        an instance of the `Language` class."""
        languages = []
        for code in map(itemgetter("iso_639_1"), self._getdata("spoken_languages")):
            try:
                item = self._all_languages[code]
            except AttributeError:
                self._all_languages = self._get_all_languages()
                item = self._all_languages[code]
            languages.append(
                other_objs.Language(
                    iso_639_1=code,
                    english_name=item["english_name"],
                    original_name=item["name"],
                )
            )
        return languages

    @property
    def countries(self) -> List[other_objs.Country]:
        """Return production countries. Each item is an instance of
        the `Country` class."""
        countries = []
        for item in self._getdata("production_countries"):
            countries.append(other_objs.Country(item["iso_3166_1"], item["name"]))
        return countries

    @property
    def popularity(self) -> float:
        """Return popularity of a movie on TMDb.

        See more:
        https://developers.themoviedb.org/3/getting-started/popularity."""
        return self._getdata("popularity")

    @property
    def revenue(self) -> int:
        """Return revenue of a movie."""
        return self._getdata("revenue")

    @property
    def budget(self) -> int:
        """Return budget of a movie."""
        return self._getdata("budget")

    @property
    def runtime(self) -> int:
        """Return a movie runtime."""
        return self._getdata("runtime")

    @property
    def status(self) -> str:
        """Return one of this values: `"Rumored"`, `"Planned"`,
        `"In Production"`, `"Post Production"`, `"Released"`,
        `"Canceled"`."""
        return self._getdata("status")

    @property
    def companies(self) -> List[company_obj.Company]:
        """Return the production companies. Each item is an
        instance of the `Company` class."""

        def _c(c):
            return company_obj.Company(c["id"], **c)

        return list(map(_c, self._getdata("production_companies")))

    @property
    def cast(self) -> List[Tuple[person_obj.Person, other_objs.Credit]]:
        """Return movie cast as list of tuples `(Person, Credit)`."""
        cast = []
        for item in self._getdata("credits")["cast"]:
            kwargs = {
                "credit_type": "cast",
                "media_type": "movie",
                "department": "Acting",
                "job": "Actor",
            }
            credit = other_objs.Credit(
                item["credit_id"],
                media_data=self.data,
                character=item["character"],
                **kwargs,
            )
            person = person_obj.Person(item["id"], **item)
            cast.append((person, credit))
        return cast

    @property
    def crew(self) -> List[Tuple[person_obj.Person, other_objs.Credit]]:
        """Return movie crew as list of tuples `(Person, Credit)`."""
        crew = []
        for item in self._getdata("credits")["crew"]:
            kwargs = {
                "credit_type": "crew",
                "media_type": "movie",
                "department": item["department"],
                "job": item["job"],
            }
            credit = other_objs.Credit(
                item["credit_id"], media_data=self.data, **kwargs
            )
            person = person_obj.Person(item["id"], **item)
            crew.append((person, credit))
        return crew

    @property
    def vote(self) -> other_objs.Vote:
        """Return an instance of the `Vote` class. It is like a
        `NamedTuple` object with two attributes: `average` and
        `count`."""
        average = self._getdata("vote_average")
        count = self._getdata("vote_count")
        return other_objs.Vote(average=average, count=count)

    @property
    def videos(self) -> List[other_objs.Video]:
        """Return videos. Each item is an instance of the `Video`
        class."""
        videos = []
        for item in self._getdata("videos")["results"]:
            url = f"https://www.youtube.com/watch?v={item['key']}"
            videos.append(
                other_objs.Video(name=item["name"], type=item["type"], url=url)
            )
        return videos

    @property
    def genres(self) -> List[other_objs.Genre]:
        """Return a movie genres."""

        def _g(g):
            return other_objs.Genre(tmdb_id=g["id"], name=g["name"])

        return list(map(_g, self._getdata("genres")))

    @property
    def keywords(self) -> List[other_objs.Keyword]:
        """Return a movie keywords."""

        def _k(k):
            return other_objs.Keyword(k["id"], **k)

        return list(map(_k, self._getdata("keywords")["keywords"]))

    @property
    def imdb_id(self) -> Optional[str]:
        """Return the ID of a movie on IMDb."""
        return self._getdata("external_ids")["imdb_id"]

    @property
    def facebook_id(self) -> Optional[str]:
        """Return the ID of a movie on Facebook."""
        return self._getdata("external_ids")["facebook_id"]

    @property
    def instagram_id(self) -> Optional[str]:
        """Return the ID of a movie on Instagram."""
        return self._getdata("external_ids")["instagram_id"]

    @property
    def twitter_id(self) -> Optional[str]:
        """Return the ID of a movie on Twitter."""
        return self._getdata("external_ids")["twitter_id"]

    def get_all(self, **params) -> dict:
        """Get all information about a movie. This method
        makes only one API request."""
        methods = ",".join(URL.ALL_MOVIE_SECOND_SUFFIXES)
        all_data = self.get_details(**{"append_to_response": methods, **params})
        self.data.update(all_data)
        return all_data

    def get_details(self, **params) -> dict:
        """Get the primary information about a movie."""
        details = self._request(
            URL.MOVIE_DETAILS.format(movie_id=self.tmdb_id), **params
        )
        self.data.update(details)
        return details

    def get_alternative_titles(self, **params) -> dict:
        """Get all of the alternative titles for a movie."""
        alternative_titles = self._request(
            URL.MOVIE_ALTERNATIVE_TITLES.format(movie_id=self.tmdb_id), **params
        )
        self.data.update({"alternative_titles": alternative_titles})
        return alternative_titles

    def get_changes(self, **params) -> dict:
        """Get the changes for a movie. By default only the
        last 24 hours are returned."""
        changes = self._request(
            URL.MOVIE_CHANGES.format(movie_id=self.tmdb_id), **params
        )
        self.data.update({"changes": changes})
        return changes

    def get_credits(self, **params) -> dict:
        """Get the cast and crew for a movie."""
        credits = self._request(
            URL.MOVIE_CREDITS.format(movie_id=self.tmdb_id), **params
        )
        self.data.update({"credits": credits})
        return credits

    def get_external_ids(self, **params) -> dict:
        """Get the external ids for a movie. Such as
        Facebook, Instagram, Twitter and IMDb"""
        external_ids = self._request(
            URL.MOVIE_EXTERNAL_IDS.format(movie_id=self.tmdb_id), **params
        )
        self.data.update({"external_ids": external_ids})
        return external_ids

    def get_images(self, **params) -> dict:
        """Get the images that belong to a movie."""
        images = self._request(URL.MOVIE_IMAGES.format(movie_id=self.tmdb_id), **params)
        self.data.update({"images": images})
        return images

    def get_keywords(self, **params) -> dict:
        """Get the keywords that have been added to a movie."""
        keywords = self._request(
            URL.MOVIE_KEYWORDS.format(movie_id=self.tmdb_id), **params
        )
        self.data.update({"keywords": keywords})
        return keywords

    def get_release_dates(self, **params) -> dict:
        """Get the release date along with the certification
        for a movie."""
        release_dates = self._request(
            URL.MOVIE_RELEASE_DATES.format(movie_id=self.tmdb_id), **params
        )
        self.data.update({"release_dates": release_dates})
        return release_dates

    def get_videos(self, **params) -> dict:
        """Get the videos that have been added to a movie."""
        videos = self._request(URL.MOVIE_VIDEOS.format(movie_id=self.tmdb_id), **params)
        self.data.update({"videos": videos})
        return videos

    def get_translations(self, **params) -> dict:
        """Get a list of translations that have been created
        for a movie."""
        translations = self._request(
            URL.MOVIE_TRANSLATIONS.format(movie_id=self.tmdb_id), **params
        )
        self.data.update({"translations": translations})
        return translations

    def iter_recommendations(self, **params) -> Iterator[dict]:
        """Get a list of recommended movies for a movie."""
        yield from self._iter_request(
            URL.MOVIE_RECOMMENDATIONS.format(movie_id=self.tmdb_id), **params
        )

    def iter_similar_movies(self, **params) -> Iterator[dict]:
        """Get a list of recommended movies for a movie."""
        yield from self._iter_request(
            URL.MOVIE_SIMILAR.format(movie_id=self.tmdb_id), **params
        )

    def iter_reviews(self, **params) -> Iterator[dict]:
        """Get the user reviews for a movie."""
        yield from self._iter_request(
            URL.MOVIE_REVIEWS.format(movie_id=self.tmdb_id), **params
        )

    def iter_lists(self, **params) -> Iterator[dict]:
        """Get a list of lists that this movie belongs to."""
        yield from self._iter_request(
            URL.MOVIE_LISTS.format(movie_id=self.tmdb_id), **params
        )
