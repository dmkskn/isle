import pytest

import themoviedb
from themoviedb.objects.others import Genre


def test_get_movie_genres():
    r = themoviedb.get_movie_genres()
    assert isinstance(r, list)


def test_get_show_genres():
    r = themoviedb.get_show_genres()
    assert isinstance(r, list)


def test_get_genre_objects():
    movie_genres = themoviedb.get_movie_genres(objects=True)
    show_genres = themoviedb.get_show_genres(objects=True)
    assert isinstance(movie_genres[0], Genre)
    assert isinstance(show_genres[0], Genre)
