import pytest

import isle
from isle.objects import Genre


def test_get_movie_genres():
    r = isle.get_movie_genres()
    assert isinstance(r, list)


def test_get_show_genres():
    r = isle.get_show_genres()
    assert isinstance(r, list)


def test_get_genre_objects():
    movie_genres = isle.get_movie_genres(objects=True)
    show_genres = isle.get_show_genres(objects=True)
    assert isinstance(movie_genres[0], Genre)
    assert isinstance(show_genres[0], Genre)
