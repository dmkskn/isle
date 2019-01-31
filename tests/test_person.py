import inspect
from itertools import islice

import pytest

import isle.people
from isle import Person


def test_get_latest():
    person = isle.people.get_latest()
    assert isinstance(person, Person)


def test_get_popular():
    shows = isle.people.get_popular()
    assert inspect.isgenerator(shows)
    person = next(shows)
    assert isinstance(person, Person)
