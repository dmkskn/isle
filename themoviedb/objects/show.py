from __future__ import annotations

from typing import Iterator, List, Optional, Tuple

import themoviedb._urls as URL
import themoviedb.objects._tmdb as _tmdb_obj
import themoviedb.objects.company as company
import themoviedb.objects.others as other_objs
import themoviedb.objects.person as person_obj

from .._config import tmdb_api_key


class Show(_tmdb_obj.TMDb):
    """Represents a TV show."""

    def _init(self):
        return self.get_all()

    @property
    def title(self) -> dict:
        """Return titles of a TV show in different languages.
        Each key is an ISO-3166-1 code (such as `"US"`, `"RU"`,
        etc.), and the value is the corresponding title.

        There is two special keys: `"original"` and `"default"`.
        The first one returns the original movie title and the
        second one depends on the location."""

        def _n(n):
            return n["iso_3166_1"], n["data"]["name"]

        names = {}
        names["default"] = self._getdata("name")
        names["original"] = self._getdata("original_name")
        for k, v in map(_n, self._getdata("translations")["translations"]):
            names[k] = v
        return names

    @property
    def overview(self) -> dict:
        """Return the overviews of a TV show in different
        languages. Each key is an ISO-3166-1 code (such as `"US"`,
        `"RU"`, etc.), and the value is the corresponding overview.

        There is a key `"default"`. It depends on the location."""

        def _o(o):
            return o["iso_3166_1"], o["data"]["overview"]

        overviews = {}
        overviews["default"] = self._getdata("overview")
        for k, v in map(_o, self._getdata("translations")["translations"]):
            overviews[k] = v
        return overviews

    @property
    def homepage(self) -> dict:
        """Return a TV show homepages. Each key is an ISO-3166-1
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
            pages[k] = v
        return pages

    @property
    def creators(self) -> List[person_obj.Person]:
        """Return the creators of a TV show."""

        def _c(c):
            return person_obj.Person(c["id"], **c)

        return [c for c in map(_c, self._getdata("created_by"))]

    @property
    def backdrops(self) -> List[other_objs.Image]:
        """Return backdrops that belong to a TV show. Each item
        is an instance of the `Image` class."""

        def _i(i):
            return other_objs.Image(i, type_="backdrop")

        return list(map(_i, self._getdata("images")["backdrops"]))

    @property
    def posters(self) -> List[other_objs.Image]:
        """Return posters that belong to a TV show. Each item is
        an instance of the `Image` class."""

        def _i(i):
            return other_objs.Image(i, type_="poster")

        return list(map(_i, self._getdata("images")["posters"]))

    @property
    def runtimes(self) -> List[int]:
        """Return the running times of TV show episodes."""
        return self._getdata("episode_run_time")

    @property
    def first_air_date(self) -> str:
        """Return the air date of the first episode."""
        return self._getdata("first_air_date")

    @property
    def last_air_date(self) -> str:
        """Return the air date of the last episode."""
        return self._getdata("last_air_date")

    @property
    def in_production(self) -> bool:
        """Return `True` if a TV show is in production."""
        return self._getdata("in_production")

    @property
    def languages(self) -> List[other_objs.Language]:
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
                other_objs.Language(
                    iso_639_1=code,
                    english_name=item["english_name"],
                    original_name=item["name"],
                )
            )
        return languages

    @property
    def last_episode(self) -> Episode:
        """Return the last episode."""
        item = self._getdata("last_episode_to_air")
        return Episode(
            item["episode_number"],
            show_id=self.tmdb_id,
            season_number=item["season_number"],
        )

    @property
    def next_episode(self) -> Episode:
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
    def n_episodes(self) -> int:
        """Return the number of episodes."""
        return self._getdata("number_of_episodes")

    @property
    def n_seasons(self) -> int:
        """Return the number of seasons."""
        return self._getdata("number_of_seasons")

    @property
    def countries(self) -> List[other_objs.Country]:
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
                    other_objs.Country(iso_3166_1=code, english_name=english_name)
                )
            else:
                continue
        return countries

    @property
    def popularity(self) -> float:
        """Return popularity of a TV show on TMDb.

        See more:
        https://developers.themoviedb.org/3/getting-started/popularity."""
        return self._getdata("popularity")

    @property
    def companies(self) -> List[company.Company]:
        """Return the production companies. Each item is an
        instance of the `Company` class."""

        def _c(c):
            return company.Company(c["id"], **c)

        return list(map(_c, self._getdata("production_companies")))

    @property
    def seasons(self) -> List[Season]:
        """Return seasons. Each item is an instance of the `Season`
        class."""
        seasons = []
        for item in self._getdata("seasons"):
            seasons.append(Season(item["season_number"], show_id=self.tmdb_id, **item))
        return seasons

    @property
    def status(self) -> str:
        return self._getdata("status")

    @property
    def type(self) -> str:
        return self._getdata("type")

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
        """Return a TV show genres."""

        def _g(g):
            return other_objs.Genre(tmdb_id=g["id"], name=g["name"])

        return list(map(_g, self._getdata("genres")))

    @property
    def keywords(self) -> List[other_objs.Keyword]:
        """Return a TV show keywords."""

        def _k(k):
            return other_objs.Keyword(k["id"], **k)

        return list(map(_k, self._getdata("keywords")["results"]))

    @property
    def imdb_id(self) -> Optional[str]:
        """Return the ID of a TV show on IMDb."""
        return self._getdata("external_ids")["imdb_id"]

    @property
    def tvdb_id(self) -> Optional[str]:
        """Return the ID of a TV show on TVDb."""
        return self._getdata("external_ids")["tvdb_id"]

    @property
    def facebook_id(self) -> Optional[str]:
        """Return the ID of a TV show on Facebook."""
        return self._getdata("external_ids")["facebook_id"]

    @property
    def instagram_id(self) -> Optional[str]:
        """Return the ID of a TV show on Instagram."""
        return self._getdata("external_ids")["instagram_id"]

    @property
    def twitter_id(self) -> Optional[str]:
        """Return the ID of a TV show on Twitter."""
        return self._getdata("external_ids")["twitter_id"]

    @property
    def ratings(self) -> dict:
        """Return content ratings (certifications) that have been
        added to a TV show. Each key is an ISO-3166-1
        code (such as `"US"`, `"RU"`, etc.) and the value is the
        corresponding rating."""
        ratings = {}
        for item in self._getdata("content_ratings")["results"]:
            ratings[item["iso_3166_1"]] = item["rating"]
        return ratings

    @property
    def cast(self) -> List[Tuple[person_obj.Person, other_objs.Credit]]:
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
            credit = other_objs.Credit(
                item["credit_id"], media_data=self.data, **kwargs
            )
            person = person_obj.Person(item["id"], **item)
            crew.append((person, credit))
        return crew

    def _get_all_countries(self):
        data = self._request(URL.COUNTRIES_CONFIGURATION, **{"api_key": tmdb_api_key()})
        countries = {}
        for item in data:
            countries[item["iso_3166_1"]] = item["english_name"]
        return countries

    def get_all(self, **params):
        """Get all information about a TV show. This method
        makes only one API request."""
        methods = ",".join(URL.ALL_SHOW_SECOND_SUFFIXES)
        all_data = self.get_details(**{"append_to_response": methods, **params})
        self.data.update(all_data)
        return all_data

    def get_details(self, **params) -> dict:
        """Get the primary information about a TV show."""
        details = self._request(URL.SHOW_DETAILS.format(show_id=self.tmdb_id), **params)
        self.data.update(details)
        return details

    def get_alternative_titles(self, **params) -> dict:
        """Get all of the alternative titles for a TV show."""
        alternative_titles = self._request(
            URL.SHOW_ALTERNATIVE_TITLES.format(show_id=self.tmdb_id), **params
        )
        self.data.update({"alternative_titles": alternative_titles})
        return alternative_titles

    def get_changes(self, **params) -> dict:
        """Get the changes for a TV show. By default only the
        last 24 hours are returned."""
        changes = self._request(URL.SHOW_CHANGES.format(show_id=self.tmdb_id), **params)
        self.data.update({"changes": changes})
        return changes

    def get_content_ratings(self, **params) -> dict:
        """Get the list of content ratings (certifications)
        that have been added to a TV show."""
        content_ratings = self._request(
            URL.SHOW_CONTENT_RATINGS.format(show_id=self.tmdb_id), **params
        )
        self.data.update({"content_ratings": content_ratings})
        return content_ratings

    def get_credits(self, **params) -> dict:
        """Get the cast and crew for a TV show."""
        credits = self._request(URL.SHOW_CREDITS.format(show_id=self.tmdb_id), **params)
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

    def get_external_ids(self, **params) -> dict:
        """Get the external ids for a TV show. Such as
        Facebook, Instagram, Twitter, IMDb and TVDB"""
        external_ids = self._request(
            URL.SHOW_EXTERNAL_IDS.format(show_id=self.tmdb_id), **params
        )
        self.data.update({"external_ids": external_ids})
        return external_ids

    def get_images(self, **params) -> dict:
        """Get the images that belong to a TV show."""
        images = self._request(URL.SHOW_IMAGES.format(show_id=self.tmdb_id), **params)
        self.data.update({"images": images})
        return images

    def get_keywords(self, **params) -> dict:
        """Get the keywords that have been added to a TV show."""
        keywords = self._request(
            URL.SHOW_KEYWORDS.format(show_id=self.tmdb_id), **params
        )
        self.data.update({"keywords": keywords})
        return keywords

    def iter_recommendations(self, **params) -> Iterator[dict]:
        """Get a list of recommended movies for a TV show."""
        yield from self._iter_request(
            URL.SHOW_RECOMMENDATIONS.format(show_id=self.tmdb_id), **params
        )

    def iter_reviews(self, **params) -> Iterator[dict]:
        """Get the user reviews for a TV show."""
        yield from self._iter_request(
            URL.SHOW_REVIEWS.format(show_id=self.tmdb_id), **params
        )

    def get_screened_theatrically(self, **params):
        """Get a list of seasons or episodes that have been
        screened in a film festival or theatre."""
        screened_theatrically = self._request(
            URL.SHOW_SCREENED_THEATRICALLY.format(show_id=self.tmdb_id), **params
        )
        self.data.update({"screened_theatrically": screened_theatrically})
        return screened_theatrically

    def iter_similar_shows(self, **params) -> Iterator[dict]:
        """Get a list of recommended movies for a TV shows."""
        yield from self._iter_request(
            URL.SHOW_SIMILAR.format(show_id=self.tmdb_id), **params
        )

    def get_translations(self, **params) -> dict:
        """Get a list of the translations that exist for a
        TV show."""
        translations = self._request(
            URL.SHOW_TRANSLATIONS.format(show_id=self.tmdb_id), **params
        )
        self.data.update({"translations": translations})
        return translations

    def get_videos(self, **params) -> dict:
        """Get the videos that have been added to a TV show."""
        videos = self._request(URL.SHOW_VIDEOS.format(show_id=self.tmdb_id), **params)
        self.data.update({"videos": videos})
        return videos


class Season(_tmdb_obj.TMDb):
    """Represents a TV show season."""

    def __init__(self, n: int, *, show_id: int, **kwargs):
        self.data = {"season_number": n, **kwargs}
        self.show_id = show_id
        self.number = self.data["season_number"]
        self.n_requests = 0

    def _init(self):
        self.get_all()

    @property
    def tmdb_id(self) -> int:
        """Return the ID of a season on TMDb."""
        return self._getdata("id")

    @property
    def n(self) -> int:
        """Return a season number."""
        return self._getdata("season_number")

    @property
    def title(self) -> str:
        """Return a season's name."""
        return self._getdata("name")

    @property
    def overview(self) -> str:
        """Return a season's overview."""
        return self._getdata("overview")

    @property
    def air_date(self) -> str:
        """Return the air date of a season."""
        return self._getdata("air_date")

    @property
    def episodes(self) -> List[Episode]:
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
    def tvdb_id(self) -> Optional[str]:
        """Return the ID of a season on TVDb."""
        return self._getdata("external_ids")["tvdb_id"]

    @property
    def posters(self) -> List[other_objs.Image]:
        """Return poster images that belong to a season. Each item
        is an instance of the `Image` class."""

        def _i(i):
            return other_objs.Image(i, type_="poster")

        return list(map(_i, self._getdata("images")["posters"]))

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
    def cast(self) -> List[Tuple[person_obj.Person, other_objs.Credit]]:
        """Return TV season cast as list of tuples `(Person, Credit)`."""
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
        """Return a TV season crew as list of tuples `(Person, Credit)`."""
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

    def get_all(self, **params):
        """Get all information about a TV season in a single
        response."""
        methods = ",".join(URL.ALL_SEASON_SECOND_SUFFIXES)
        all_data = self.get_details(**{"append_to_response": methods, **params})
        self.data.update(all_data)
        return all_data

    def get_details(self, **params) -> dict:
        """Get the primary TV season details."""
        details = self._request(
            URL.SEASON_DETAILS.format(show_id=self.show_id, season_number=self.number),
            **params,
        )
        self.data.update(details)
        return details

    def get_changes(self, **params) -> dict:
        """Get the changes for a TV season. By default only the
        last 24 hours are returned."""
        changes = self._request(
            URL.SEASON_CHANGES.format(season_id=self.tmdb_id), **params
        )
        self.data.update({"changes": changes})
        return changes

    def get_credits(self, **params) -> dict:
        """Get the credits for TV season."""
        movie_credits = self._request(
            URL.SEASON_CREDITS.format(show_id=self.show_id, season_number=self.number),
            **params,
        )
        self.data.update({"credits": movie_credits})
        return movie_credits

    def get_external_ids(self, **params) -> dict:
        """Get the external ids for a TV season."""
        external_ids = self._request(
            URL.SEASON_EXTERNAL_IDS.format(
                show_id=self.show_id, season_number=self.number
            ),
            **params,
        )
        self.data.update({"external_ids": external_ids})
        return external_ids

    def get_images(self, **params) -> dict:
        """Get the images that belong to a TV season."""
        images = self._request(
            URL.SEASON_IMAGES.format(show_id=self.show_id, season_number=self.number),
            **params,
        )
        self.data.update({"images": images})
        return images

    def get_videos(self, **params) -> dict:
        """Get the videos that have been added to a TV season."""
        videos = self._request(
            URL.SEASON_VIDEOS.format(show_id=self.show_id, season_number=self.number),
            **params,
        )
        self.data.update({"videos": videos})
        return videos


class Episode(_tmdb_obj.TMDb):
    """Represents a TV show episode."""

    def __init__(self, n, *, show_id, season_number, **kwargs):
        self.data = {"episode_number": n, "season_number": season_number, **kwargs}
        self.show_id = show_id
        self.number = self.data["episode_number"]
        self.season_number = self.data["season_number"]
        self.n_requests = 0

    def _init(self):
        self.get_all()

    @property
    def tmdb_id(self) -> int:
        """Return the ID of an episode on TMDb."""
        return self._getdata("id")

    @property
    def tvdb_id(self) -> Optional[str]:
        """Return the ID of an episode on TVDb."""
        return self._getdata("external_ids")["tvdb_id"]

    @property
    def imdb_id(self) -> Optional[str]:
        """Return the ID of an episode on IMDb."""
        return self._getdata("external_ids")["imdb_id"]

    @property
    def air_date(self) -> str:
        """Return the air date of an episode."""
        return self._getdata("air_date")

    @property
    def n(self) -> int:
        """Return an episode number."""
        return self._getdata("episode_number")

    @property
    def sn(self) -> int:
        """Return a season number."""
        return self._getdata("season_number")

    @property
    def title(self) -> dict:
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
    def overview(self) -> dict:
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
    def stills(self) -> List[other_objs.Image]:
        """Return images that belong to an episode. Each item is
        an instance of the `Image` class."""

        def _i(i):
            return other_objs.Image(i, type_="still")

        return list(map(_i, self._getdata("images")["stills"]))

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
    def vote(self) -> other_objs.Vote:
        """Return an instance of the `Vote` class. It is like a
        `NamedTuple` object with two attributes: `average` and
        `count`."""
        average = self._getdata("vote_average")
        count = self._getdata("vote_average")
        return other_objs.Vote(average=average, count=count)

    @property
    def cast(self) -> List[Tuple[person_obj.Person, other_objs.Credit]]:
        """Return TV episode cast as list of tuples
        `(Person, Credit)`."""
        cast = []
        for item in self._getdata("credits")["cast"]:
            kwargs = {"credit_type": "cast", "department": "Acting", "job": "Actor"}
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
        """Return TV episode crew as list of tuples
        `(Person, Credit)`."""
        crew = []
        for item in self._getdata("credits")["crew"]:
            kwargs = {
                "credit_type": "crew",
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
    def guest_stars(self) -> List[Tuple[person_obj.Person, other_objs.Credit]]:
        """Return TV episode guest stars as list of tuples
        `(Person, Credit)`."""
        guest_stars = []
        for item in self._getdata("credits")["guest_stars"]:
            credit = other_objs.Credit(
                item["credit_id"], media_data=self.data, character=item.get("character")
            )
            person = person_obj.Person(item["id"], **item)
            guest_stars.append((person, credit))
        return guest_stars

    def get_all(self, **params):
        """Get all information about a TV episode in a single
        response."""
        methods = ",".join(URL.ALL_EPISODE_SECOND_SUFFIXES)
        all_data = self.get_details(**{"append_to_response": methods, **params})
        self.data.update(all_data)
        return all_data

    def get_details(self, **params) -> dict:
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

    def get_changes(self, **params) -> dict:
        """Get the changes for a TV episode. By default only the
        last 24 hours are returned."""
        changes = self._request(
            URL.EPISODE_CHANGES.format(episode_id=self.tmdb_id), **params
        )
        self.data.update({"changes": changes})
        return changes

    def get_credits(self, **params) -> dict:
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

    def get_external_ids(self, **params) -> dict:
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

    def get_images(self, **params) -> dict:
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

    def get_videos(self, **params) -> dict:
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

    def get_translations(self, **params) -> dict:
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