import pytest

from themoviedb.objects.others import Genre


GENRE_ID = 12
GENRE_NM = "Adventure"


@pytest.fixture
def genre():
    return Genre(tmdb_id=GENRE_ID, name=GENRE_NM)


def test_genre_id(genre: Genre):
    assert genre.tmdb_id == GENRE_ID
    assert genre.tmdb_id == genre[0]


def test_genre_name(genre: Genre):
    assert genre.name == GENRE_NM
    assert genre.name == genre[1]


def test_genre_to_str(genre: Genre):
    assert str(genre) == genre.name
