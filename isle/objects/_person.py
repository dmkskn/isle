from typing import Iterator, List, Optional, Tuple, Union

import isle._urls as URL
import isle.objects._tmdb as _tmdb_obj
import isle.objects._movie as movie_obj
import isle.objects._others as other_objs
import isle.objects._show as show_obj


__all__ = ["Person"]


class Person(_tmdb_obj.TMDb):
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
            credit = other_objs.Credit(
                item["credit_id"],
                person_data=self.data,
                character=item["character"],
                **kwargs,
            )
            movie = movie_obj.Movie(item["id"], **item)
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
            credit = other_objs.Credit(
                item["credit_id"], person_data=self.data, **kwargs
            )
            movie = movie_obj.Movie(item["id"], **item)
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
            credit = other_objs.Credit(
                item["credit_id"],
                person_data=self.data,
                character=item["character"],
                **kwargs,
            )
            show = show_obj.Show(item["id"], **item)
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
            credit = other_objs.Credit(
                item["credit_id"], person_data=self.data, **kwargs
            )
            show = show_obj.Show(item["id"], **item)
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
            credit = other_objs.Credit(
                item["credit_id"],
                person_data=self.data,
                character=item["character"],
                **kwargs,
            )
            Obj = (
                show_obj.Show
                if item["media_type"] == "tv"
                else movie_obj.Movie
            )
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
            credit = other_objs.Credit(
                item["credit_id"], person_data=self.data, **kwargs
            )
            Obj = (
                show_obj.Show
                if item["media_type"] == "tv"
                else movie_obj.Movie
            )
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
            return other_objs.Image(i, type_="profile")

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
