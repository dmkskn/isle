import inspect
import re

import pytest

from themoviedb.objects.movie import Movie
from themoviedb.objects.person import Person
from themoviedb.objects.show import Show
from themoviedb.objects.others import (
    Country,
    Credit,
    Genre,
    Image,
    Keyword,
    Language,
    Video,
    Vote,
)


PERSON_ID = 287


@pytest.fixture
def empty_person():
    person = Person(PERSON_ID)
    assert person.data.keys() == {"id"}
    return person


@pytest.fixture(scope="module")
def person():
    person = Person(PERSON_ID)
    person._init()
    return person


def test_caching_to_data(empty_person: Person):
    assert empty_person.data == {"id": empty_person.tmdb_id}
    data = empty_person.get_all()
    assert empty_person.data == data


def test_raise_error_when_init_without_id():
    with pytest.raises(TypeError):
        _ = Person()  # pylint: disable=E1120


def test_name_attr(person: Person):
    assert isinstance(person.name, str)
    assert person.name == person.data["name"]


def test_also_known_as_attr(person: Person):
    assert isinstance(person.also_known_as, list)
    assert all(isinstance(item, str) for item in person.also_known_as)


def test_birthday_attr(person: Person):
    assert isinstance(person.birthday, str)
    assert re.match(r"\d{4}-\d{2}-\d{2}", person.birthday)


def test_known_for_department_attr(person: Person):
    assert isinstance(person.known_for_department, str)
    assert person.data["known_for_department"] == person.known_for_department


def test_deathday_attr(person: Person):
    assert isinstance(person.deathday, (str, type(None)))


def test_gender_attr(person: Person):
    assert isinstance(person.gender, int)


def test_biography_attr(person: Person):
    biography = person.biography
    assert isinstance(biography, dict)
    assert "default" in biography
    assert all(len(key) == 2 for key in filter(str.isupper, biography))
    assert all(biography[key] for key in filter(str.isupper, biography))


def test_homepage_attr(person: Person):
    assert isinstance(person.homepage, (str, type(None)))


def test_popularity_attr(person: Person):
    assert isinstance(person.popularity, float)


def test_place_of_birth_attr(person: Person):
    assert isinstance(person.place_of_birth, str)


def test_is_adult_attr(person: Person):
    assert isinstance(person.is_adult, bool)


def test_movie_cast_attr(person: Person):
    assert isinstance(person.movie_cast, list)
    movie, credit = person.movie_cast[0]
    assert isinstance(movie, Movie)
    assert isinstance(credit, Credit)


def test_movie_crew_attr(person: Person):
    assert isinstance(person.movie_crew, list)
    movie, credit = person.movie_crew[0]
    assert isinstance(movie, Movie)
    assert isinstance(credit, Credit)


def test_show_cast_attr(person: Person):
    assert isinstance(person.show_cast, list)
    show, credit = person.show_cast[0]
    assert isinstance(show, Show)
    assert isinstance(credit, Credit)


def test_show_crew_attr(person: Person):
    assert isinstance(person.show_crew, list)
    show, credit = person.show_crew[0]
    assert isinstance(show, Show)
    assert isinstance(credit, Credit)


def test_cast_attr(person: Person):
    assert isinstance(person.cast, list)
    item, credit = person.cast[0]
    assert isinstance(item, (Show, Movie))
    assert isinstance(credit, Credit)


def test_crew_attr(person: Person):
    assert isinstance(person.crew, list)
    item, credit = person.crew[0]
    assert isinstance(item, (Show, Movie))
    assert isinstance(credit, Credit)


def test_external_ids_attrs(person: Person):
    assert person.imdb_id == person.data["external_ids"]["imdb_id"]
    assert person.freebase_mid == person.data["external_ids"]["freebase_mid"]
    assert person.freebase_id == person.data["external_ids"]["freebase_id"]
    assert person.tvrage_id == person.data["external_ids"]["tvrage_id"]
    assert person.facebook_id == person.data["external_ids"]["facebook_id"]
    assert person.instagram_id == person.data["external_ids"]["instagram_id"]
    assert person.twitter_id == person.data["external_ids"]["twitter_id"]


def test_posters_attr(person: Person):
    assert isinstance(person.profiles, list)
    assert all(isinstance(item, Image) for item in person.profiles)
    assert person.profiles[0]._type == "profile"


def test_get_details(empty_person: Person):
    details = empty_person.get_details()
    assert isinstance(details, dict)
    assert empty_person.data == details


def test_get_changes(empty_person: Person):
    changes = empty_person.get_changes()
    assert empty_person.data["changes"] == changes


def test_get_movie_credits(empty_person: Person):
    credits = empty_person.get_movie_credits()
    assert credits == empty_person.data["movie_credits"]


def test_get_show_credits(empty_person: Person):
    credits = empty_person.get_show_credits()
    assert credits == empty_person.data["tv_credits"]


def test_get_combined_credits(empty_person: Person):
    credits = empty_person.get_combined_credits()
    assert credits == empty_person.data["combined_credits"]


def test_get_external_ids(empty_person: Person):
    external_ids = empty_person.get_external_ids()
    assert external_ids == empty_person.data["external_ids"]


def test_get_images(empty_person: Person):
    images = empty_person.get_images()
    assert images == empty_person.data["images"]


def test_get_translations(empty_person: Person):
    translations = empty_person.get_translations()
    assert translations == empty_person.data["translations"]


def test_iter_tagged_images(empty_person: Person):
    tagged_images = empty_person.iter_tagged_images()
    assert inspect.isgenerator(tagged_images)
    item = next(tagged_images)
    assert isinstance(item, dict)
