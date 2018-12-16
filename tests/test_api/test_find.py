import pytest

import isle
from isle import Movie, Person, Episode, Season, Show


URL = "https://api.themoviedb.org/3/find/{}?"
IMDB_MOVIE_ID = "tt0046438"
IMDB_SHOW_ID = "tt4574334"
IMDB_PERSON_ID = "nm0000093"
TVDB_EPISODE_ID = 5_468_124
TVDB_SEASON_ID = 651_264


def test_find_movie():
    results = isle.find(IMDB_MOVIE_ID, src="imdb_id")
    assert len(results["movie_results"]) == 1
    assert isinstance(results["movie_results"][0], Movie)
    assert results["movie_results"][0].imdb_id == IMDB_MOVIE_ID


def test_find_show():
    results = isle.find(IMDB_SHOW_ID, src="imdb_id")
    assert len(results["tv_results"]) == 1
    assert isinstance(results["tv_results"][0], Show)
    assert results["tv_results"][0].imdb_id == IMDB_SHOW_ID


def test_find_person():
    results = isle.find(IMDB_PERSON_ID, src="imdb_id")
    assert len(results["person_results"]) == 1
    assert isinstance(results["person_results"][0], Person)
    assert results["person_results"][0].imdb_id == IMDB_PERSON_ID


def test_find_episode():
    results = isle.find(TVDB_EPISODE_ID, src="tvdb_id")
    assert len(results["tv_episode_results"]) == 1
    assert isinstance(results["tv_episode_results"][0], Episode)
    assert results["tv_episode_results"][0].tvdb_id == TVDB_EPISODE_ID


def test_find_season():
    results = isle.find(TVDB_SEASON_ID, src="tvdb_id")
    assert len(results["tv_season_results"]) == 1
    assert isinstance(results["tv_season_results"][0], Season)
    assert results["tv_season_results"][0].tvdb_id == TVDB_SEASON_ID
