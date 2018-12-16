import pytest

from isle.objects import Image


DATA = {
    "aspect_ratio": 1.777_777_777_777_78,
    "file_path": "/fCayJrkfRaCRCTh8GqN30f8oyQF.jpg",
    "height": 720,
    "iso_639_1": None,
    "vote_average": 0,
    "vote_count": 0,
    "width": 1280,
}


@pytest.fixture
def image():
    return Image(DATA, type_="backdrop")


def test_raises_error_when_init_without_type():
    with pytest.raises(TypeError):
        _ = Image(DATA)  # pylint: disable=E1125


def test_get_urls(image: Image):
    assert image._configs_data == {}
    assert isinstance(image.url, dict)
    assert image._configs_data != {}


def test_get_sizes(image: Image):
    assert image._configs_data == {}
    assert isinstance(image.sizes, list)
    assert image.sizes == image._configs_data["backdrop_sizes"]
