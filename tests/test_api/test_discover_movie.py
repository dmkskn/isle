import pytest
import inspect
import json
import os
from urllib.parse import urlencode
from urllib.request import urlopen

import isle
from isle.objects.movie import Movie


URL = "https://api.themoviedb.org/3/discover/movie?"
OPTIONS = {
    "sort_by": "popularity.desc",
    "with_crew": 488,  # Steven Spielberg
    "with_cast": 3,  # Harrison Ford
}


@pytest.fixture(scope="module")
def n_results():
    params = urlencode({"api_key": os.environ["TMDB_API_KEY"], **OPTIONS})
    response = urlopen(f"{URL}{params}")
    response = json.loads(response.read().decode("utf-8"))
    return response["total_results"]


@pytest.fixture(scope="module")
def results():
    results = isle.discover_movies(OPTIONS)
    items = list(results)
    return items, results


def test_output_is_generator(results):
    assert inspect.isgenerator(results[1])


def test_output_item_is_Movie_instance(results):
    item = results[0][0]
    assert isinstance(item, Movie)


def test_amount_of_results(results, n_results):
    assert len(list(results[0])) == n_results
