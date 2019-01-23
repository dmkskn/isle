import pytest

from isle.objects import Credit, Movie, Person, Show


PERSON_ID = 287
MOVIE_ID = 18148
SHOW_ID = 1399
MOVIE_CREDIT_ID = "52fe47639251416c750978a9"
SHOW_CREDIT_ID = "5256c8af19c2956ff60479f6"


@pytest.fixture
def empty_movie_credit():
    return Credit(MOVIE_CREDIT_ID)


@pytest.fixture
def empty_show_credit():
    return Credit(SHOW_CREDIT_ID)


@pytest.fixture
def movie_credit():
    credit = Credit(MOVIE_CREDIT_ID)
    credit._init()
    return credit


@pytest.fixture
def show_credit(empty_show_credit):
    credit = Credit(SHOW_CREDIT_ID)
    credit._init()
    return credit


def test_raises_error_when_init_without_id():
    with pytest.raises(TypeError):
        _ = Credit()  # pylint: disable=E1120


def test_credit_created_from_movie_object():
    movie = Movie(MOVIE_ID)
    all_movie_data = movie.get_all()
    _, credit = movie.crew[0]
    assert isinstance(credit, Credit)
    assert credit._media_data == movie.data == all_movie_data


def test_credit_created_from_person_object():
    person = Person(PERSON_ID)
    all_person_data = person.get_all()
    _, credit = person.cast[0]
    assert isinstance(credit, Credit)
    assert credit._person_data == person.data == all_person_data


def test_get_details(movie_credit: Credit, show_credit: Credit):
    details = movie_credit.get_details()
    assert isinstance(details, dict)
    assert all(key in details for key in ["media", "person", "job"])

    details = show_credit.get_details()
    assert isinstance(details, dict)
    assert all(key in details for key in ["media", "person", "job"])


def test_media_type_attr(movie_credit: Credit, show_credit: Credit):
    assert movie_credit.media_type in ["movie", "tv"]
    assert show_credit.media_type in ["movie", "tv"]


def test_type_attr(movie_credit: Credit, show_credit: Credit):
    assert movie_credit.type in ["crew", "cast"]
    assert show_credit.type in ["crew", "cast"]


def test_department_attr(movie_credit: Credit):
    assert isinstance(movie_credit.department, str)


def test_job_attr(movie_credit: Credit):
    assert isinstance(movie_credit.job, str)


def test_character_attr(show_credit: Credit):
    assert isinstance(show_credit.character, str)


def test_person_attr(movie_credit: Credit):
    assert isinstance(movie_credit.person, Person)


def test_media_attr(movie_credit: Credit, show_credit: Credit):
    assert isinstance(movie_credit.media, Movie)
    assert isinstance(show_credit.media, Show)


def test_eq(movie_credit):
    assert Credit(MOVIE_CREDIT_ID) == movie_credit


def test_not_eq(movie_credit, show_credit):
    assert movie_credit != show_credit
