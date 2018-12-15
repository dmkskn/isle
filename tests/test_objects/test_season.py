import pytest

from isle.objects.others import Credit, Image, Video
from isle.objects.person import Person
from isle.objects.show import Episode, Season


SHOW_ID = 66732
SEASON_N = 1


@pytest.fixture
def empty_season():
    return Season(SEASON_N, show_id=SHOW_ID)


@pytest.fixture(scope="module")
def season():
    season = Season(SEASON_N, show_id=SHOW_ID)
    season._init()
    return season


def test_caching_to_data(empty_season: Season):
    assert empty_season.data == {"season_number": empty_season.n}
    data = empty_season.get_all()
    assert empty_season.data == data


def test_repr(season):
    assert season.__repr__() == f"Season({season.tmdb_id})"


def test_raise_error_when_init_without_args():
    with pytest.raises(TypeError):
        _ = Season()  # pylint: disable=E1120,E1125


def test_raise_error_when_init_without_show_id():
    with pytest.raises(TypeError):
        _ = Season(SEASON_N)  # pylint: disable=E1125


def test_raise_error_if_show_id_is_not_kwarg():
    with pytest.raises(TypeError):
        _ = Season(SEASON_N, SHOW_ID)  # pylint: disable=E1125,E1121


def test_tmdb_id_attr(season: Season):
    assert isinstance(season.tmdb_id, int)


def test_tvdb_id_attr(season: Season):
    assert isinstance(season.tvdb_id, int)


def test_number_attr(season: Season):
    assert isinstance(season.number, int)
    assert season.number == season.n


def test_title_attr(season: Season):
    assert isinstance(season.title, str)


def test_overview_attr(season: Season):
    assert isinstance(season.overview, str)


def test_air_date_attr(season: Season):
    assert isinstance(season.air_date, str)
    assert len(season.air_date.split("-")) == 3


def test_episodes_attr(season: Season):
    assert isinstance(season.episodes, list)
    assert all(isinstance(item, Episode) for item in season.episodes)


def test_posters_attr(season: Season):
    assert isinstance(season.posters, list)
    assert all(isinstance(item, Image) for item in season.posters)


def test_videos_attr(season: Season):
    assert isinstance(season.videos, list)
    assert all(isinstance(item, Video) for item in season.videos)


def test_cast_attr(season: Season):
    assert isinstance(season.cast, list)
    person, credit = season.cast[0]
    assert isinstance(person, Person)
    assert isinstance(credit, Credit)


def test_crew_attr(season: Season):
    assert isinstance(season.crew, list)
    person, credit = season.crew[0]
    assert isinstance(person, Person)
    assert isinstance(credit, Credit)


def test_get_details(empty_season: Season):
    details = empty_season.get_details()
    assert isinstance(details, dict)
    assert empty_season.data == details


def test_get_changes(empty_season: Season):
    changes = empty_season.get_changes()
    assert empty_season.data["changes"] == changes


def test_get_credits(empty_season: Season):
    credits = empty_season.get_credits()
    assert empty_season.data["credits"] == credits


def test_get_external_ids(empty_season: Season):
    external_ids = empty_season.get_external_ids()
    assert empty_season.data["external_ids"] == external_ids


def test_get_videos(empty_season: Season):
    videos = empty_season.get_videos()
    assert empty_season.data["videos"] == videos
