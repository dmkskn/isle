import inspect

import pytest

from isle.objects import Keyword, Movie


KEYWORD_ID = 3417
KEYWORD_NM = "wormhole"


@pytest.fixture
def keyword_without_name():
    keyword = Keyword(KEYWORD_ID)
    assert keyword.data.keys() == {"id"}
    return keyword


@pytest.fixture
def keyword_with_name():
    keyword = Keyword(KEYWORD_ID, name=KEYWORD_NM)
    assert keyword.data.keys() == {"id", "name"}
    return keyword


@pytest.fixture(scope="module")
def test_repr(keyword_without_name: Keyword):
    keyword = keyword_without_name
    assert keyword.__repr__() == f"Keyword({keyword.id_})"


def test_init_keyword_with_name(keyword_with_name: Keyword):
    assert keyword_with_name.data == {"id": KEYWORD_ID, "name": KEYWORD_NM}


def test_init_keyword_without_name(keyword_without_name: Keyword):
    keyword = keyword_without_name
    assert keyword.data == {"id": KEYWORD_ID}


def test_get_details(keyword_without_name: Keyword):
    details = keyword_without_name.get_details()
    assert details == keyword_without_name.data


def test_iter_movies(keyword_with_name: Keyword):
    movies = keyword_with_name.iter_movies()
    assert inspect.isgenerator(movies)
    item = next(movies)
    assert isinstance(item, Movie)


def test_keyword_to_str(keyword_with_name, keyword_without_name):
    assert str(keyword_with_name) == keyword_with_name.name
    assert str(keyword_without_name) == keyword_without_name.name


def test_eq(keyword_with_name, keyword_without_name):
    assert keyword_with_name == keyword_without_name


def test_not_eq(keyword_with_name, keyword_without_name):
    keyword_without_name.tmdb_id = 1234
    assert keyword_with_name != keyword_without_name
