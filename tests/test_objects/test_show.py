import inspect

import pytest

from isle import Company, Person, Episode, Season, Show
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

SHOW_ID = 1399


@pytest.fixture
def empty_show():
    show = Show(SHOW_ID)
    assert show.data.keys() == {"id"}
    return show


@pytest.fixture(scope="module")
def show():
    show = Show(SHOW_ID)
    show._init()
    return show


def test_caching_to_data(empty_show: Show):
    assert empty_show.data == {"id": empty_show.tmdb_id}
    data = empty_show.get_all()
    assert empty_show.data == data


def test_repr(show: Show):
    assert show.__repr__() == f"Show({show.tmdb_id})"


def test_raise_error_when_init_without_id():
    with pytest.raises(TypeError):
        _ = Show()  # pylint: disable=E1120


def test_title_attr(show: Show):
    assert isinstance(show.title, dict)
    assert all(key in show.title for key in ["original", "default"])
    assert all(len(key) == 2 for key in filter(str.isupper, show.title))
    assert all(show.title[key] for key in filter(str.isupper, show.title))


def test_overview_attr(show: Show):
    assert isinstance(show.overview, dict)
    assert "default" in show.overview
    assert all(len(key) == 2 for key in filter(str.isupper, show.overview))
    assert all(
        show.overview[key] for key in filter(str.isupper, show.overview)
    )


def test_creators_attr(show: Show):
    assert isinstance(show.creators, list)
    assert all(isinstance(item, Person) for item in show.creators)


def test_runtimes_attr(show: Show):
    assert isinstance(show.runtimes, list)
    assert all(isinstance(item, int) for item in show.runtimes)


def test_first_air_date_attr(show: Show):
    assert isinstance(show.first_air_date, str)


def test_last_air_date_attr(show: Show):
    assert isinstance(show.last_air_date, str)


def test_homepage_attr(show: Show):
    assert isinstance(show.homepage, dict)
    assert "default" in show.homepage


def test_in_production_attr(show: Show):
    assert isinstance(show.in_production, bool)


def test_languages_attr(show: Show):
    assert isinstance(show.languages, list)
    assert all(isinstance(item, Language) for item in show.languages)


def test_last_episode_attr(show: Show):
    assert isinstance(show.last_episode, Episode)


def test_next_episode_attr(show: Show):
    assert isinstance(show.next_episode, (Episode, type(None)))


def test_n_episodes_attr(show: Show):
    assert isinstance(show.n_episodes, int)


def test_n_seasons_attr(show: Show):
    assert isinstance(show.n_seasons, int)


def test_countries_attr(show: Show):
    assert isinstance(show.countries, list)
    assert all(isinstance(item, Country) for item in show.countries)


def test_popularity_attr(show: Show):
    assert isinstance(show.popularity, float)


def test_companies_attr(show: Show):
    assert isinstance(show.companies, list)
    assert all(isinstance(item, Company) for item in show.companies)


def test_seasons_attr(show: Show):
    assert isinstance(show.seasons, list)
    assert all(isinstance(item, Season) for item in show.seasons)


def test_status_attr(show: Show):
    assert isinstance(show.status, str)


def test_vote_attr(show: Show):
    assert isinstance(show.vote, Vote)


def test_ratings_attr(show: Show):
    assert isinstance(show.ratings, dict)
    assert all(len(code) == 2 for code in show.ratings)
    assert all(isinstance(rating, str) for rating in show.ratings.values())


def test_cast_attr(show: Show):
    assert isinstance(show.cast, list)
    person, credit = show.cast[0]
    assert isinstance(person, Person)
    assert isinstance(credit, Credit)


def test_crew_attr(show: Show):
    assert isinstance(show.crew, list)
    person, credit = show.crew[0]
    assert isinstance(person, Person)
    assert isinstance(credit, Credit)


def test_external_ids_attrs(show: Show):
    assert show.imdb_id == show.data["external_ids"]["imdb_id"]
    assert show.tvdb_id == show.data["external_ids"]["tvdb_id"]
    assert show.facebook_id == show.data["external_ids"]["facebook_id"]
    assert show.instagram_id == show.data["external_ids"]["instagram_id"]
    assert show.twitter_id == show.data["external_ids"]["twitter_id"]


def test_backdrops_attr(show: Show):
    assert isinstance(show.backdrops, list)
    assert all(isinstance(item, Image) for item in show.backdrops)
    assert show.backdrops[0]._type == "backdrop"


def test_posters_attr(show: Show):
    assert isinstance(show.posters, list)
    assert all(isinstance(item, Image) for item in show.posters)
    assert show.posters[0]._type == "poster"


def test_keywords_attr(show: Show):
    assert isinstance(show.keywords, list)
    assert all(isinstance(item, Keyword) for item in show.keywords)


def test_genres_attr(show: Show):
    assert isinstance(show.genres, list)
    assert all(isinstance(item, Genre) for item in show.genres)


def test_videos_attr(show: Show):
    assert isinstance(show.videos, list)
    assert all(isinstance(item, Video) for item in show.videos)


def test_get_details(empty_show: Show):
    details = empty_show.get_details()
    assert details == empty_show.data


def test_get_alternative_titles(empty_show: Show):
    titles = empty_show.get_alternative_titles()
    assert titles == empty_show.data["alternative_titles"]


def test_get_changes(empty_show: Show):
    changes = empty_show.get_changes()
    assert changes == empty_show.data["changes"]


def test_get_content_ratings(empty_show: Show):
    rating = empty_show.get_content_ratings()
    assert rating == empty_show.data["content_ratings"]


def test_get_credits(empty_show: Show):
    credits = empty_show.get_credits()
    assert credits == empty_show.data["credits"]


def test_get_episode_groups(empty_show: Show):
    episode_groups = empty_show.get_episode_groups()
    assert episode_groups == empty_show.data["episode_groups"]


def test_get_external_ids(empty_show: Show):
    external_ids = empty_show.get_external_ids()
    assert external_ids == empty_show.data["external_ids"]


def test_get_images(empty_show: Show):
    images = empty_show.get_images()
    assert images == empty_show.data["images"]


def test_get_keywords(empty_show: Show):
    keywords = empty_show.get_keywords()
    assert keywords == empty_show.data["keywords"]


def test_get_screened_theatrically(empty_show: Show):
    screened = empty_show.get_screened_theatrically()
    assert screened == empty_show.data["screened_theatrically"]


def test_get_translations(empty_show: Show):
    translations = empty_show.get_translations()
    assert translations == empty_show.data["translations"]


def test_get_videos(empty_show: Show):
    videos = empty_show.get_videos()
    assert videos == empty_show.data["videos"]


def test_iter_recommendations(empty_show: Show):
    recommendations = empty_show.iter_recommendations()
    assert inspect.isgenerator(recommendations)
    item = next(recommendations)
    assert isinstance(item, dict)


def test_iter_reviews(empty_show: Show):
    reviews = empty_show.iter_reviews()
    assert inspect.isgenerator(reviews)
    item = next(reviews)
    assert isinstance(item, dict)


def test_iter_similar_shows(empty_show: Show):
    similar_shows = empty_show.iter_similar_shows()
    assert inspect.isgenerator(similar_shows)
    item = next(similar_shows)
    assert isinstance(item, dict)


def test_eq(show: Show, empty_show: Show):
    assert show == empty_show


def test_not_eq(show: Show, empty_show: Show):
    show.tmdb_id = 1234
    assert show != empty_show
