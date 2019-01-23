import inspect
from itertools import islice

import pytest

import isle.movie
from isle import Movie


def test_get_latest():
    movie = isle.movie.get_latest()
    assert isinstance(movie, Movie)


def test_get_popular():
    movies = isle.movie.get_popular()
    assert inspect.isgenerator(movies)
    movie = next(movies)
    assert isinstance(movie, Movie)


def test_get_top_rated():
    movies = isle.movie.get_top_rated()
    assert inspect.isgenerator(movies)
    movie = next(movies)
    assert isinstance(movie, Movie)


def test_get_upcoming():
    movies = isle.movie.get_upcoming()
    assert inspect.isgenerator(movies)
    movie = next(movies)
    assert isinstance(movie, Movie)


def test_get_now_playing():
    movies = isle.movie.get_now_playing()
    assert inspect.isgenerator(movies)
    movie = next(movies)
    assert isinstance(movie, Movie)
