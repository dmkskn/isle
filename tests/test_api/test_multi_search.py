import inspect
import json
import os
from urllib.parse import urlencode
from urllib.request import urlopen

import pytest

import isle
from isle import Movie, Show, Person

URL = "https://api.themoviedb.org/3/search/multi?"
QUERY = "Spielberg"


@pytest.fixture(scope="module")
def n_results():
    params = urlencode(
        {
            "api_key": os.environ["TMDB_API_KEY"],
            "language": "en-US",
            "include_adult": "false",
            "query": QUERY,
            "page": 1,
        }
    )
    response = urlopen(f"{URL}{params}")
    response = json.loads(response.read().decode("utf-8"))
    return response["total_results"]


@pytest.fixture(scope="module")
def results():
    results = isle.multi_search(QUERY)
    items = list(results)
    return items, results


def test_output_is_generator(results):
    assert inspect.isgenerator(results[1])


def test_output_item_type(results):
    assert all(isinstance(item, (Movie, Show, Person)) for item in results[0])


def test_output_has_Person_objects(results):
    assert any([isinstance(item, Person) for item in results[0]])


def test_output_has_Movie_objects(results):
    assert any([isinstance(item, Movie) for item in results[0]])


def test_output_has_Show_objects(results):
    assert any([isinstance(item, Show) for item in results[0]])


def test_query_is_required():
    with pytest.raises(TypeError):
        isle.search_movie(**{"language": "en-US"})


def test_amount_of_results(results, n_results):
    assert len(list(results[0])) == n_results
