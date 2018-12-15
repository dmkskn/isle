import pytest
import inspect

from isle.objects._tmdb import TMDb


MOVIE_ID = 18148

GET_URL = f"https://api.themoviedb.org/3/movie/{MOVIE_ID}"
GET_ITER_URL = f"https://api.themoviedb.org/3/movie/{MOVIE_ID}/reviews"
# POST_URL = ...
# DELETE_URL = ...


@pytest.fixture
def tmdb():
    TMDb.__abstractmethods__ = frozenset()
    return TMDb(MOVIE_ID)  # pylint: disable=E0110


def test_request(tmdb: TMDb):
    r = tmdb._request(GET_URL, **{})
    assert r["original_title"] == "東京物語"


def test_iter_request(tmdb: TMDb):
    r = tmdb._iter_request(GET_ITER_URL, **{})
    assert inspect.isgenerator(r)
    assert isinstance(next(r), dict)


# def test_post_request(tmdb: TMDb):
#     pass


# def test_delete_request(tmdb: TMDb):
#     pass


def test_n_requests(tmdb: TMDb):
    assert tmdb.n_requests == 0

    tmdb._request(GET_URL, **{})
    assert tmdb.n_requests == 1

    tmdb._request(GET_URL, **{})
    assert tmdb.n_requests == 2

    tmdb._iter_request(GET_ITER_URL, **{})
    assert tmdb.n_requests == 3

    tmdb._iter_request(GET_ITER_URL, **{})
    assert tmdb.n_requests == 4

    # tmdb._delete_request(DELETE_URL, **{})
    # assert tmdb.n_requests == 5

    # tmdb._post_request(POST_URL, **{})
    # assert tmdb.n_requests == 6
