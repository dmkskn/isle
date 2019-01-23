import inspect
import os

import pytest

from isle.objects import Account, Episode, Movie, Show, TMDbList


USERNAME = os.getenv("TMDB_USERNAME")
PASSWORD = os.getenv("TMDB_PASSWORD")


@pytest.fixture
def account():
    return Account()


@pytest.fixture
def logged_in_account():
    account = Account()
    account.login(USERNAME, PASSWORD)
    return account


@pytest.fixture(scope="module")
def once_logged_in_account():
    account = Account()
    account.login(USERNAME, PASSWORD)
    return account


def test_login(account):
    r = account.login(USERNAME, PASSWORD)
    assert r["success"] is True


def test_logout(logged_in_account):
    r = logged_in_account.logout()
    assert r["success"] is True


def test_saves_session_id(account, once_logged_in_account):
    with pytest.raises(account.SessionError):
        _ = account._session_id
    assert isinstance(once_logged_in_account._session, account._Session)


def test_saves_token_id(account, once_logged_in_account):
    with pytest.raises(account.TokenError):
        _ = account._token_id
    assert isinstance(once_logged_in_account._token, account._Token)


def test_get_details(once_logged_in_account):
    details = once_logged_in_account.get_details()
    assert isinstance(details, dict)
    assert all(x in details for x in ["avatar", "name", "username"])


def test_properties(once_logged_in_account):
    assert isinstance(once_logged_in_account.username, str)
    assert isinstance(once_logged_in_account.fallback_language, str)
    assert isinstance(once_logged_in_account.default_language, str)


def test_properties_download_once(logged_in_account):
    n = logged_in_account.n_requests
    _ = logged_in_account.username
    assert logged_in_account.n_requests == n + 1


def test_iter_lists(once_logged_in_account):
    lists = once_logged_in_account.iter_lists()
    assert inspect.isgenerator(lists)
    assert all(isinstance(x, TMDbList) for x in lists)


def test_iter_favorite_movies(once_logged_in_account):
    favorite_movies = once_logged_in_account.iter_favorite_movies()
    assert inspect.isgenerator(favorite_movies)
    assert all(isinstance(x, Movie) for x in favorite_movies)


def test_iter_favorite_shows(once_logged_in_account):
    favorite_shows = once_logged_in_account.iter_favorite_shows()
    assert inspect.isgenerator(favorite_shows)
    assert all(isinstance(x, Show) for x in favorite_shows)


def test_iter_rated_movies(once_logged_in_account):
    rated_movies = once_logged_in_account.iter_rated_movies()
    assert inspect.isgenerator(rated_movies)
    assert all(isinstance(x, Movie) for x in rated_movies)


def test_iter_rated_shows(once_logged_in_account):
    rated_shows = once_logged_in_account.iter_rated_shows()
    assert inspect.isgenerator(rated_shows)
    assert all(isinstance(x, Show) for x in rated_shows)


def test_iter_rated_episodes(once_logged_in_account):
    rated_episodes = once_logged_in_account.iter_rated_episodes()
    assert inspect.isgenerator(rated_episodes)
    assert all(isinstance(x, Episode) for x in rated_episodes)


def test_iter_movie_watchlist(once_logged_in_account):
    movie_watchlist = once_logged_in_account.iter_movie_watchlist()
    assert inspect.isgenerator(movie_watchlist)
    assert all(isinstance(x, Movie) for x in movie_watchlist)


def test_iter_show_watchlist(once_logged_in_account):
    show_watchlist = once_logged_in_account.iter_show_watchlist()
    assert inspect.isgenerator(show_watchlist)
    assert all(isinstance(x, Movie) for x in show_watchlist)


def test_mark_as_favorite(once_logged_in_account):
    once_logged_in_account.remove_from_favorites(Movie(18148))
    r = once_logged_in_account.mark_as_favorite(Movie(18148))
    assert r["status_code"] == 1


def test_remove_from_favorite(once_logged_in_account):
    once_logged_in_account.mark_as_favorite(Movie(18148))
    r = once_logged_in_account.remove_from_favorites(Movie(18148))
    assert r["status_code"] == 13


def test_add_to_watchlist(once_logged_in_account):
    once_logged_in_account.remove_from_watchlist(Movie(18148))
    r = once_logged_in_account.add_to_watchlist(Movie(18148))
    assert r["status_code"] == 1


def test_remove_from_watchlist(once_logged_in_account):
    once_logged_in_account.add_to_watchlist(Movie(18148))
    r = once_logged_in_account.remove_from_watchlist(Movie(18148))
    assert r["status_code"] == 13


def test_rate(once_logged_in_account):
    once_logged_in_account.delete_rating(Movie(18148))
    r = once_logged_in_account.rate(Movie(18148), 8.5)
    assert r["status_code"] == 1


def test_delete_rating(once_logged_in_account):
    once_logged_in_account.rate(Movie(18148), 8.5)
    r = once_logged_in_account.delete_rating(Movie(18148))
    assert r["status_code"] == 13


def test_eq(logged_in_account, once_logged_in_account):
    assert logged_in_account == once_logged_in_account
