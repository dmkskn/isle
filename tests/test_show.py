import inspect
from itertools import islice

import pytest

import isle.show
from isle import Show


def test_get_latest():
    show = isle.show.get_latest()
    assert isinstance(show, Show)


def test_get_popular():
    shows = isle.show.get_popular()
    assert inspect.isgenerator(shows)
    show = next(shows)
    assert isinstance(show, Show)


def test_get_top_rated():
    shows = isle.show.get_top_rated()
    assert inspect.isgenerator(shows)
    show = next(shows)
    assert isinstance(show, Show)


def test_get_airing_today():
    shows = isle.show.get_airing_today()
    assert inspect.isgenerator(shows)
    show = next(shows)
    assert isinstance(show, Show)


def test_get_on_the_air():
    shows = isle.show.get_on_the_air()
    assert inspect.isgenerator(shows)
    show = next(shows)
    assert isinstance(show, Show)
