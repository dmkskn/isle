import inspect
import os
import json
from urllib.parse import urlencode
from urllib.request import urlopen

import pytest

import isle
from isle import Person


URL = "https://api.themoviedb.org/3/search/person?"
NAME = "Abrams"


@pytest.fixture(scope="module")
def n_results():
    params = urlencode(
        {
            "api_key": os.environ["TMDB_API_KEY"],
            "language": "en-US",
            "include_adult": "false",
            "query": NAME,
            "page": 1,
        }
    )
    response = urlopen(f"{URL}{params}")
    response = json.loads(response.read().decode("utf-8"))
    return response["total_results"]


@pytest.fixture(scope="module")
def results():
    results = isle.search_person(NAME)
    items = list(results)
    return items, results


def test_output_is_generator(results):
    assert inspect.isgenerator(results[1])


def test_output_item_is_Person_instance(results):
    item = results[0][0]
    assert isinstance(item, Person)


def test_name_is_required():
    with pytest.raises(TypeError):
        isle.search_person(**{"language": "en-US"})


def test_all_args_except_the_first_one_are_kwargs():
    with pytest.raises(TypeError):
        isle.search_movie(NAME, True)  # pylint: disable=E1121


def test_amount_of_results(results, n_results):
    assert len(list(results[0])) == n_results
