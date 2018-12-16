import pytest

from isle import Person, Episode
from isle.objects import Credit, Image, Video, Vote


SHOW_ID = 66732
SEASON_N = 1
EPISODE_N = 1


@pytest.fixture
def empty_episode():
    return Episode(EPISODE_N, show_id=SHOW_ID, season_number=SEASON_N)


@pytest.fixture(scope="module")
def episode():
    episode = Episode(EPISODE_N, show_id=SHOW_ID, season_number=SEASON_N)
    episode._init()
    return episode


def test_raise_error_when_init_without_attrs():
    with pytest.raises(TypeError):
        _ = Episode()  # pylint: disable=E1120,E1125


def test_raise_error_when_init_only_with_episode_number():
    with pytest.raises(TypeError):
        _ = Episode(EPISODE_N)  # pylint: disable=E1125


def test_raise_error_when_show_id_is_not_kwarg():
    with pytest.raises(TypeError):
        _ = Episode(EPISODE_N, SHOW_ID)  # pylint: disable=E1121,E1125


def test_raise_error_when_init_only_with_episode_number_and_show_id():
    with pytest.raises(TypeError):
        _ = Episode(EPISODE_N, show_id=SHOW_ID)  # pylint: disable=E1121,E1125


def test_tvdb_id_attr(episode: Episode):
    assert episode.tvdb_id == episode.data["external_ids"]["tvdb_id"]


def test_caching_to_data(empty_episode: Episode):
    assert empty_episode.data == {
        "episode_number": EPISODE_N,
        "season_number": SEASON_N,
    }
    data = empty_episode.get_all()
    assert empty_episode.data == data


def test_tmdb_id_attr(episode: Episode):
    assert isinstance(episode.tmdb_id, int)
    assert episode.tmdb_id != SHOW_ID


def test_number_attr(episode: Episode):
    assert isinstance(episode.number, int)
    assert episode.number == episode.n


def test_season_number_attr(episode: Episode):
    assert isinstance(episode.season_number, int)
    assert episode.season_number == episode.sn


def test_title_attr(episode: Episode):
    titles = episode.title
    assert isinstance(titles, dict)
    assert "default" in titles
    assert all(len(key) == 2 for key in filter(str.isupper, titles))
    assert all(titles[key] for key in filter(str.isupper, titles))


def test_overview_attr(episode: Episode):
    overviews = episode.overview
    assert isinstance(overviews, dict)
    assert "default" in overviews
    assert all(len(key) == 2 for key in filter(str.isupper, overviews))
    assert all(overviews[key] for key in filter(str.isupper, overviews))


def test_air_date_attr(episode: Episode):
    assert isinstance(episode.air_date, str)
    assert len(episode.air_date.split("-")) == 3


def test_stills_attr(episode: Episode):
    assert isinstance(episode.stills, list)
    assert all(isinstance(item, Image) for item in episode.stills)
    assert episode.stills[0]._type == "still"


def test_videos_attr(episode: Episode):
    assert isinstance(episode.videos, list)
    assert all(isinstance(item, Video) for item in episode.videos)


def test_cast_attr(episode: Episode):
    assert isinstance(episode.cast, list)
    person, credit = episode.cast[0]
    assert isinstance(person, Person)
    assert isinstance(credit, Credit)


def test_crew_attr(episode: Episode):
    assert isinstance(episode.crew, list)
    person, credit = episode.crew[0]
    assert isinstance(person, Person)
    assert isinstance(credit, Credit)


def test_guest_stars_attr(episode: Episode):
    assert isinstance(episode.guest_stars, list)
    person, credit = episode.guest_stars[0]
    assert isinstance(person, Person)
    assert isinstance(credit, Credit)


def test_vote_attr(episode: Episode):
    assert isinstance(episode.vote, Vote)


def test_get_all(empty_episode: Episode):
    data = empty_episode.get_all()
    assert data == empty_episode.data


def test_get_details(empty_episode: Episode):
    details = empty_episode.get_details()
    assert details == empty_episode.data


def test_get_changes(empty_episode: Episode):
    changes = empty_episode.get_changes()
    assert changes == empty_episode.data["changes"]


def test_get_external_ids(empty_episode: Episode):
    external_ids = empty_episode.get_external_ids()
    assert external_ids == empty_episode.data["external_ids"]


def test_get_credits(empty_episode: Episode):
    credits = empty_episode.get_credits()
    assert credits == empty_episode.data["credits"]


def test_get_images(empty_episode: Episode):
    images = empty_episode.get_images()
    assert images == empty_episode.data["images"]


def test_get_videos(empty_episode: Episode):
    videos = empty_episode.get_videos()
    assert videos == empty_episode.data["videos"]
