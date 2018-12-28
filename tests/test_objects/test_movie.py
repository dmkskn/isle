import inspect

import pytest

from isle import Movie, Person, Company
from isle.objects import (
    Country,
    Credit,
    Genre,
    Image,
    Keyword,
    Language,
    Video,
    Vote,
)


MOVIE_ID = 18148


@pytest.fixture
def empty_movie():
    return Movie(MOVIE_ID)


@pytest.fixture(scope="module")
def movie():
    movie = Movie(MOVIE_ID)
    movie._init()
    return movie


def test_caching_to_data(empty_movie: Movie):
    assert empty_movie.data == {"id": empty_movie.tmdb_id}
    data = empty_movie.get_all()
    assert empty_movie.data == data


def test_repr(movie: Movie):
    assert movie.__repr__(), f"Movie({movie.movie_id})"


def test_raise_error_when_init_without_id():
    with pytest.raises(TypeError):
        _ = Movie()  # pylint: disable=E1120


def test_title_attr(movie: Movie):
    titles = movie.title
    assert isinstance(titles, dict)
    assert all(key in titles for key in ["default", "original"])
    assert all(len(key) == 2 for key in filter(str.isupper, titles))
    assert all(titles[key] for key in filter(str.isupper, titles))


def test_overview_attr(movie: Movie):
    overviews = movie.overview
    assert "default" in overviews
    assert all(len(key) == 2 for key in filter(str.isupper, overviews))
    assert all(overviews[key] for key in filter(str.isupper, overviews))


def test_tagline_attr(movie: Movie):
    assert isinstance(movie.tagline, str)


def test_year_attr(movie: Movie):
    year = movie.year
    assert isinstance(year, int)
    assert len(str(year)) == 4


def test_external_ids_attrs(movie: Movie):
    assert movie.imdb_id == movie.data["external_ids"]["imdb_id"]
    assert movie.facebook_id == movie.data["external_ids"]["facebook_id"]
    assert movie.instagram_id == movie.data["external_ids"]["instagram_id"]
    assert movie.twitter_id == movie.data["external_ids"]["twitter_id"]


def test_releases_attr(movie: Movie):
    releases = movie.releases
    assert isinstance(releases, dict)
    assert all(len(key) == 2 for key in filter(str.isupper, releases))
    assert all(
        isinstance(releases[key], list)
        for key in filter(str.isupper, releases)
    )


def test_is_adult_attr(movie: Movie):
    assert isinstance(movie.is_adult, bool)


def test_backdrops_attr(movie: Movie):
    assert isinstance(movie.backdrops, list)
    assert all(isinstance(item, Image) for item in movie.backdrops)
    assert movie.backdrops[0]._type == "backdrop"


def test_posters_attr(movie: Movie):
    assert isinstance(movie.posters, list)
    assert all(isinstance(item, Image) for item in movie.posters)
    assert movie.posters[0]._type == "poster"


def test_languages_attr(movie: Movie):
    assert isinstance(movie.languages, list)
    assert all(isinstance(item, Language) for item in movie.languages)


def test_popularity_attr(movie: Movie):
    assert isinstance(movie.popularity, float)


def test_homepage_attr(movie: Movie):
    pages = movie.homepage
    assert isinstance(pages, dict)
    assert "default" in pages if pages else True
    assert all(len(key) == 2 for key in filter(str.isupper, pages))
    assert all(pages[key] for key in filter(str.isupper, pages))


def test_revenue_attr(movie: Movie):
    assert isinstance(movie.revenue, int)


def test_budget_attr(movie: Movie):
    assert isinstance(movie.budget, int)


def test_runtime_attr(movie: Movie):
    assert isinstance(movie.runtime, int)


def test_status_attr(movie: Movie):
    assert isinstance(movie.status, str)


def test_cast_attr(movie: Movie):
    assert isinstance(movie.cast, list)
    person, credit = movie.cast[0]
    assert isinstance(person, Person)
    assert isinstance(credit, Credit)


def test_crew_attr(movie: Movie):
    assert isinstance(movie.crew, list)
    person, credit = movie.crew[0]
    assert isinstance(person, Person)
    assert isinstance(credit, Credit)


def test_videos_attr(movie: Movie):
    assert isinstance(movie.videos, list)
    assert all(isinstance(item, Video) for item in movie.videos)


def test_keywords_attr(movie: Movie):
    assert isinstance(movie.keywords, list)
    assert all(isinstance(item, Keyword) for item in movie.keywords)


def test_genres_attr(movie: Movie):
    assert isinstance(movie.genres, list)
    assert all(isinstance(item, Genre) for item in movie.genres)


def test_companies_attr(movie: Movie):
    assert isinstance(movie.genres, list)
    assert all(isinstance(item, Company) for item in movie.companies)


def test_vote_attr(movie: Movie):
    assert isinstance(movie.vote, Vote)


def test_countries_attr(movie: Movie):
    assert isinstance(movie.countries, list)
    assert all(isinstance(item, Country) for item in movie.countries)


def test_get_details(empty_movie: Movie):
    details = empty_movie.get_details()
    assert isinstance(details, dict)
    assert empty_movie.data == details


def test_get_alternative_titles(empty_movie: Movie):
    titles = empty_movie.get_alternative_titles()
    assert isinstance(titles, dict)
    assert empty_movie.data["alternative_titles"] == titles


def test_get_changes(empty_movie: Movie):
    changes = empty_movie.get_changes()
    assert empty_movie.data["changes"] == changes


def test_get_credits(empty_movie: Movie):
    credits = empty_movie.get_credits()
    assert empty_movie.data["credits"] == credits


def test_get_external_ids(empty_movie: Movie):
    external_ids = empty_movie.get_external_ids()
    assert empty_movie.data["external_ids"] == external_ids


def test_get_keywords(empty_movie: Movie):
    keywords = empty_movie.get_keywords()
    assert empty_movie.data["keywords"] == keywords


def test_get_images(empty_movie: Movie):
    images = empty_movie.get_images()
    assert empty_movie.data["images"] == images


def test_get_release_dates(empty_movie: Movie):
    release_dates = empty_movie.get_release_dates()
    assert empty_movie.data["release_dates"] == release_dates


def test_get_videos(empty_movie: Movie):
    videos = empty_movie.get_videos()
    assert empty_movie.data["videos"] == videos


def test_get_translations(empty_movie: Movie):
    translations = empty_movie.get_translations()
    assert empty_movie.data["translations"] == translations


def test_iter_recommendations(empty_movie: Movie):
    recommendations = empty_movie.iter_recommendations()
    assert inspect.isgenerator(recommendations)
    item = next(recommendations)
    assert isinstance(item, dict)


def test_iter_similar_movies(empty_movie: Movie):
    similar_movies = empty_movie.iter_similar_movies()
    assert inspect.isgenerator(similar_movies)
    item = next(similar_movies)
    assert isinstance(item, dict)


def test_iter_reviews(empty_movie: Movie):
    reviews = empty_movie.iter_reviews()
    assert inspect.isgenerator(reviews)
    item = next(reviews)
    assert isinstance(item, dict)
    assert all(x in item for x in ["author", "content"])


def test_iter_lists(empty_movie: Movie):
    lists = empty_movie.iter_lists()
    assert inspect.isgenerator(lists)
    item = next(lists)
    assert isinstance(item, dict)
    assert all(x in item for x in ["description", "item_count"])


def test_eq(movie, empty_movie):
    assert movie == empty_movie


def test_not_eq(movie, empty_movie):
    movie.tmdb_id = 1234
    assert movie != empty_movie
