from abc import ABC, abstractmethod
from typing import Iterator

from ._tools import get_response, search_results_for
from .config import TMDB_API_KEY
from ._urls import (
    BASEURL,
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
)


class _BaseTMDbObject(ABC):
    def __init__(self, tmdb_id=None, *, preload=True, **kwargs):
        self.tmdb_id = tmdb_id or kwargs["id"]
        if kwargs.get("__is_first_init__", False):
            self._set_attrs(kwargs)
        elif preload:
            self._first_init()

    @abstractmethod
    def _first_init(self):
        pass

    def _set_attrs(self, kwargs):
        for key in kwargs.keys() - {"id", "__is_first_init__"}:
            assert key != "results"
            if isinstance(kwargs[key], dict) and ("results" in kwargs[key]):
                value = kwargs[key]["results"]
            else:
                value = kwargs[key]
            setattr(self, key, value)

    def _request(self, url: str, **params) -> dict:
        return get_response(url, **{"api_key": TMDB_API_KEY, **params})

    def _iter_request(self, url: str, **params):
        return search_results_for(url, {"api_key": TMDB_API_KEY, **params})


class Movie(_BaseTMDbObject):
    def _first_init(self):
        return self.get_all()

    def get_all(self, **params):
        """Get all information about a movie. This method
        makes only one API request."""
        methods = ",".join(ALL_MOVIE_SECOND_SUFFIXES)
        all_data = self.get_details(**{"append_to_response": methods, **params})
        self._set_attrs(all_data)
        return all_data

    def get_details(self, **params) -> dict:
        """Get the primary information about a movie."""
        details = self._request(
            f"{BASEURL}{MOVIE_DETAILS_SUFFIX.format(self.tmdb_id)}", **params
        )
        self._set_attrs(details)
        return details

    def get_alternative_titles(self, **params) -> dict:
        """Get all of the alternative titles for a movie."""
        alternative_titles = self._request(
            f"{BASEURL}{MOVIE_ALTERNATIVE_TITLES_SUFFIX.format(self.tmdb_id)}", **params
        )
        self._set_attrs(alternative_titles)
        return alternative_titles

    def get_changes(self, **params) -> dict:
        """Get the changes for a movie. By default only the 
        last 24 hours are returned."""
        changes = self._request(
            f"{BASEURL}{MOVIE_CHANGES_SUFFIX.format(self.tmdb_id)}", **params
        )
        self._set_attrs(changes)
        return changes

    def get_credits(self, **params) -> dict:
        """Get the cast and crew for a movie."""
        credits = self._request(
            f"{BASEURL}{MOVIE_CREDITS_SUFFIX.format(self.tmdb_id)}", **params
        )
        self._set_attrs(credits)
        return credits

    def get_external_ids(self, **params) -> dict:
        """Get the external ids for a movie. Such as 
        Facebook, Instagram, Twitter and IMDb"""
        external_ids = self._request(
            f"{BASEURL}{MOVIE_EXTERNAL_IDS_SUFFIX.format(self.tmdb_id)}", **params
        )
        self._set_attrs(external_ids)
        return external_ids

    def get_images(self, **params) -> dict:
        """Get the images that belong to a movie."""
        images = self._request(
            f"{BASEURL}{MOVIE_IMAGES_SUFFIX.format(self.tmdb_id)}", **params
        )
        self._set_attrs(images)
        return images

    def get_keywords(self, **params) -> dict:
        """Get the keywords that have been added to a movie."""
        keywords = self._request(
            f"{BASEURL}{MOVIE_KEYWORDS_SUFFIX.format(self.tmdb_id)}", **params
        )
        self._set_attrs(keywords)
        return keywords

    def get_release_dates(self, **params) -> dict:
        """Get the release date along with the certification
        for a movie."""
        release_dates = self._request(
            f"{BASEURL}{MOVIE_RELEASE_DATES_SUFFIX.format(self.tmdb_id)}", **params
        )
        self._set_attrs({"release_dates": release_dates})
        return release_dates

    def get_videos(self, **params) -> dict:
        """Get the videos that have been added to a movie."""
        videos = self._request(
            f"{BASEURL}{MOVIE_VIDEOS_SUFFIX.format(self.tmdb_id)}", **params
        )
        self._set_attrs({"videos": videos})
        return videos

    def get_translations(self, **params) -> dict:
        """Get a list of translations that have been created
        for a movie."""
        translations = self._request(
            f"{BASEURL}{MOVIE_TRANSLATIONS_SUFFIX.format(self.tmdb_id)}", **params
        )
        self._set_attrs(translations)
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


class Show(_BaseTMDbObject):
    def _first_init(self):
        return self.get_all()

    def get_all(self, **params):
        """Get all information about a TV show. This method
        makes only one API request."""
        methods = ",".join(ALL_SHOW_SECOND_SUFFIXES)
        all_data = self.get_details(**{"append_to_response": methods, **params})
        self._set_attrs(all_data)
        return all_data

    def get_details(self, **params) -> dict:
        """Get the primary information about a TV show."""
        details = self._request(
            f"{BASEURL}{SHOW_DETAILS_SUFFIX.format(self.tmdb_id)}", **params
        )
        self._set_attrs(details)
        return details

    def get_alternative_titles(self, **params) -> dict:
        """Get all of the alternative titles for a TV show."""
        alternative_titles = self._request(
            f"{BASEURL}{SHOW_ALTERNATIVE_TITLES_SUFFIX.format(self.tmdb_id)}", **params
        )
        self._set_attrs({"alternative_titles": alternative_titles})
        return alternative_titles

    def get_changes(self, **params) -> dict:
        """Get the changes for a TV show. By default only the 
        last 24 hours are returned."""
        changes = self._request(
            f"{BASEURL}{SHOW_CHANGES_SUFFIX.format(self.tmdb_id)}", **params
        )
        self._set_attrs(changes)
        return changes

    def get_content_ratings(self, **params) -> dict:
        """Get the list of content ratings (certifications)
        that have been added to a TV show."""
        content_ratings = self._request(
            f"{BASEURL}{SHOW_CONTENT_RATINGS_SUFFIX.format(self.tmdb_id)}", **params
        )
        self._set_attrs({"content_ratings": content_ratings})
        return content_ratings

    def get_credits(self, **params) -> dict:
        """Get the cast and crew for a TV show."""
        credits = self._request(
            f"{BASEURL}{SHOW_CREDITS_SUFFIX.format(self.tmdb_id)}", **params
        )
        self._set_attrs(credits)
        return credits

    def get_episode_groups(self, **params):
        """Get all of the episode groups that have been 
        created for a TV show."""
        episode_groups = self._request(
            f"{BASEURL}{SHOW_EPISODE_GROUPS_SUFFIX.format(self.tmdb_id)}", **params
        )
        self._set_attrs({"episode_groups": episode_groups})
        return episode_groups

    def get_external_ids(self, **params) -> dict:
        """Get the external ids for a TV show. Such as 
        Facebook, Instagram, Twitter, IMDb and TVDB"""
        external_ids = self._request(
            f"{BASEURL}{SHOW_EXTERNAL_IDS_SUFFIX.format(self.tmdb_id)}", **params
        )
        self._set_attrs(external_ids)
        return external_ids

    def get_images(self, **params) -> dict:
        """Get the images that belong to a TV show."""
        images = self._request(
            f"{BASEURL}{SHOW_IMAGES_SUFFIX.format(self.tmdb_id)}", **params
        )
        self._set_attrs(images)
        return images

    def get_keywords(self, **params) -> dict:
        """Get the keywords that have been added to a TV show."""
        keywords = self._request(
            f"{BASEURL}{SHOW_KEYWORDS_SUFFIX.format(self.tmdb_id)}", **params
        )
        self._set_attrs({"keywords": keywords})
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
        self._set_attrs({"screened_theatrically": screened_theatrically})
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
        self._set_attrs(translations)
        return translations

    def get_videos(self, **params) -> dict:
        """Get the videos that have been added to a TV show."""
        videos = self._request(
            f"{BASEURL}{SHOW_VIDEOS_SUFFIX.format(self.tmdb_id)}", **params
        )
        self._set_attrs({"videos": videos})
        return videos


class Person(_BaseTMDbObject):
    def _first_init(self):
        self.get_all()

    def get_all(self, **params):
        """Get all information about a person in a single
        response."""
        methods = ",".join(ALL_PERSON_SECOND_SUFFIXES)
        all_data = self.get_details(**{"append_to_response": methods, **params})
        self._set_attrs(all_data)
        return all_data

    def get_details(self, **params) -> dict:
        """Get the primary person details."""
        details = self._request(
            f"{BASEURL}{PERSON_DETAILS_SUFFIX.format(self.tmdb_id)}", **params
        )
        self._set_attrs(details)
        return details

    def get_changes(self, **params) -> dict:
        """Get the changes for a person. By default only the
        last 24 hours are returned."""
        changes = self._request(
            f"{BASEURL}{PERSON_CHANGES_SUFFIX.format(self.tmdb_id)}", **params
        )
        self._set_attrs(changes)
        return changes

    def get_movie_credits(self, **params) -> dict:
        """Get the movie credits for a person."""
        movie_credits = self._request(
            f"{BASEURL}{PERSON_MOVIE_CREDITS_SUFFIX.format(self.tmdb_id)}", **params
        )
        self._set_attrs(
            {"movie_cast": movie_credits["cast"], "movie_crew": movie_credits["crew"]}
        )
        return movie_credits

    def get_show_credits(self, **params) -> dict:
        """Get the TV show credits for a person."""
        show_credits = self._request(
            f"{BASEURL}{PERSON_SHOW_CREDITS_SUFFIX.format(self.tmdb_id)}", **params
        )
        self._set_attrs(
            {"show_cast": show_credits["cast"], "show_crew": show_credits["crew"]}
        )
        return show_credits

    def get_combined_credits(self, **params) -> dict:
        """Get the movie and TV credits together in a single
        response."""
        combined_credits = self._request(
            f"{BASEURL}{PERSON_COMBINED_CREDITS_SUFFIX.format(self.tmdb_id)}", **params
        )
        self._set_attrs(combined_credits)
        return combined_credits

    def get_external_ids(self, **params) -> dict:
        """Get the external ids for a person. Such as 
        Facebook, Instagram, Twitter and IMDb and others"""
        external_ids = self._request(
            f"{BASEURL}{PERSON_EXTERNAL_IDS_SUFFIX.format(self.tmdb_id)}", **params
        )
        self._set_attrs(external_ids)
        return external_ids

    def get_images(self, **params) -> dict:
        """Get the images for a person."""
        images = self._request(
            f"{BASEURL}{PERSON_IMAGES_SUFFIX.format(self.tmdb_id)}", **params
        )
        self._set_attrs(images)
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
        self._set_attrs(translations)
        return translations


class Company:
    def __init__(self, tmdb_id=None, **kwargs):
        self.tmdb_id = tmdb_id or kwargs["id"]
        for key in kwargs.keys() - {"id"}:
            setattr(self, key, kwargs[key])
