import pytest
import inspect
import os
import json
from urllib.parse import urlencode
from urllib.request import urlopen

import themoviedb
from themoviedb.objects.show import Show

URL = "https://api.themoviedb.org/3/discover/tv?"
OPTIONS = {"sort_by": "popularity.desc", "with_companies": 278}  # Propaganda Films


@pytest.fixture(scope="module")
def n_results():
    params = urlencode({"api_key": os.environ["TMDB_API_KEY"], **OPTIONS})
    response = urlopen(f"{URL}{params}")
    response = json.loads(response.read().decode("utf-8"))
    return response["total_results"]


@pytest.fixture(scope="module")
def results():
    results = themoviedb.discover_shows(OPTIONS)
    items = list(results)
    return items, results


def test_output_is_generator(results):
    assert inspect.isgenerator(results[1])


def test_output_item_is_Show_instance(results):
    item = results[0][0]
    assert isinstance(item, Show)


def test_amount_of_results(results, n_results):
    assert len(list(results[0])) == n_results
