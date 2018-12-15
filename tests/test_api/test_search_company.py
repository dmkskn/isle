import inspect
import os
import json
from urllib.parse import urlencode
from urllib.request import urlopen

import pytest

import themoviedb
from themoviedb.objects.company import Company


URL = "https://api.themoviedb.org/3/search/company?"
NAME = "Sony"


@pytest.fixture(scope="module")
def n_results():
    params = urlencode(
        {"api_key": os.environ["TMDB_API_KEY"], "query": NAME, "page": 1}
    )
    response = urlopen(f"{URL}{params}")
    response = json.loads(response.read().decode("utf-8"))
    return response["total_results"]


@pytest.fixture(scope="module")
def results():
    results = themoviedb.search_company(NAME)
    items = list(results)
    return items, results


def test_output_is_generator(results):
    assert inspect.isgenerator(results[1])


def test_output_item_is_Company_instance(results):
    item = results[0][0]
    assert isinstance(item, Company)


def test_name_is_required():
    with pytest.raises(TypeError):
        themoviedb.search_movie()  # pylint: disable=E1120


def test_amount_of_results(results, n_results):
    assert len(list(results[0])) == n_results
