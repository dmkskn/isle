import pytest
import inspect
import os
import json
from urllib.parse import urlencode
from urllib.request import urlopen

import isle
from isle.objects.movie import Movie


URL = "https://api.themoviedb.org/3/search/movie?"
TITLE = "harry potter"
YEAR = 1953


@pytest.fixture(scope="module")
def n_results():
    params = urlencode(
        {
            "api_key": os.environ["TMDB_API_KEY"],
            "language": "en-US",
            "include_adult": "false",
            "query": TITLE,
            "page": 1,
        }
    )
    response = urlopen(f"{URL}{params}")
    response = json.loads(response.read().decode("utf-8"))
    return response["total_results"]


@pytest.fixture(scope="module")
def results():
    results = isle.search_movie(TITLE)
    items = list(results)
    return items, results


def test_output_is_generator(results):
    assert inspect.isgenerator(results[1])


def test_output_item_is_Movie_instance(results):
    item = results[0][0]
    assert isinstance(item, Movie)


def test_title_is_required():
    with pytest.raises(TypeError):
        isle.search_movie(**{"year": YEAR})


def test_raises_error_when_year_is_not_kwarg():
    with pytest.raises(TypeError):
        isle.search_movie(TITLE, YEAR)  # pylint: disable=E1121


def test_amount_of_results(results, n_results):
    assert len(list(results[0])) == n_results
