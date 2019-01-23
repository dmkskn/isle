import os

import pytest

from isle.objects import Account, Language, Movie, Show, TMDbList


LIST_ID = os.getenv("TMDB_LIST_ID")


@pytest.fixture
def tmdb_list(scope="module"):
    tmdb_list = TMDbList(LIST_ID)
    tmdb_list.get_details()
    return tmdb_list


def test_get_details():
    tmdb_list = TMDbList(LIST_ID)
    details = tmdb_list.get_details()
    assert tmdb_list.data == details
    assert isinstance(details, dict)
    assert "name" in details


def test_name_attr(tmdb_list):
    assert tmdb_list.name == tmdb_list.data["name"]


def test_description_attr(tmdb_list):
    assert tmdb_list.description == tmdb_list.data["description"]


def test_creator_attr(tmdb_list):
    assert tmdb_list.creator == tmdb_list.data["created_by"]


def test_n_favorites_attr(tmdb_list):
    assert tmdb_list.n_favorites == tmdb_list.data["favorite_count"]


def test_items_attr(tmdb_list):
    assert all(isinstance(x, (Movie, Show)) for x in tmdb_list.items)


def test_language_attr(tmdb_list):
    assert isinstance(tmdb_list.language, Language)


def test_has_movie(tmdb_list):
    for item in tmdb_list.items:
        if isinstance(item, Movie):
            assert tmdb_list.has_movie(item)
            break


def test_eq():
    assert tmdb_list == tmdb_list


def test_not_eq(tmdb_list):
    assert TMDbList(1234) != tmdb_list
