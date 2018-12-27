import pytest
import inspect
import os
import json
from urllib.parse import urlencode
from urllib.request import urlopen

import isle
from isle.objects import Keyword


URL = "https://api.themoviedb.org/3/search/keyword?"
QUERY = "alien"


@pytest.fixture(scope="module")
def n_results():
    params = urlencode(
        {"api_key": os.environ["TMDB_API_KEY"], "query": QUERY, "page": 1}
    )
    response = urlopen(f"{URL}{params}")
    response = json.loads(response.read().decode("utf-8"))
    return response["total_results"]


@pytest.fixture(scope="module")
def results():
    results = isle.search_keyword(QUERY)
    items = list(results)
    return items, results


def test_output_is_generator(results):
    assert inspect.isgenerator(results[1])


def test_output_item_is_Keyword_instance(results):
    item = results[0][0]
    assert isinstance(item, Keyword)


def test_amount_of_results(results, n_results):
    assert len(list(results[0])) == n_results


def test_results_are_preloaded(results):
    for item in results[0]:
        assert "id" in item.data
        assert "name" in item.data
