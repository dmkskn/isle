import os
import inspect
import json
from urllib.parse import urlencode
from urllib.request import urlopen

import pytest

import isle
from isle import Show


URL = "https://api.themoviedb.org/3/search/tv?"
TITLE = "lost"
YEAR = 2004


@pytest.fixture(scope="module")
def n_results():
    params = urlencode(
        {
            "api_key": os.environ["TMDB_API_KEY"],
            "language": "en-US",
            "query": TITLE,
            "page": 1,
        }
    )
    response = urlopen(f"{URL}{params}")
    response = json.loads(response.read().decode("utf-8"))
    return response["total_results"]


@pytest.fixture(scope="module")
def results():
    results = isle.search_show(TITLE)
    items = list(results)
    return items, results


def test_output_is_generator(results):
    assert inspect.isgenerator(results[1])


def test_output_item_is_Show_instance(results):
    item = results[0][0]
    assert isinstance(item, Show)


def test_title_is_required():
    with pytest.raises(TypeError):
        isle.search_show(**{"first_air_date_year": YEAR})


def test_raises_error_when_year_is_not_kwarg():
    with pytest.raises(TypeError):
        isle.search_show(TITLE, YEAR)  # pylint: disable=E1121


def test_amount_of_results(results, n_results):
    assert len(list(results[0])) == n_results
