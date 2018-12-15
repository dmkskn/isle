import pytest

import isle
from isle.objects.others import Country, Language


def test_get_image_configurations():
    r = isle.get_image_configurations()
    assert isinstance(r, dict)
    assert "images" in r
    assert "base_url" in r["images"]


def test_get_countries():
    r = isle.get_countries()
    assert isinstance(r, list)
    assert "english_name" in r[0]


def test_get_country_objects():
    r = isle.get_countries(objects=True)
    assert isinstance(r[0], Country)


def test_get_jobs():
    r = isle.get_jobs()
    assert isinstance(r, list)
    assert isinstance(r[0], dict)
    assert "department" in r[0]


def test_get_languages():
    r = isle.get_languages()
    assert isinstance(r, list)
    assert isinstance(r[0], dict)
    assert "english_name" in r[0]
    assert "iso_639_1" in r[0]
    assert "name" in r[0]


def test_get_language_objects():
    r = isle.get_languages(objects=True)
    assert isinstance(r[0], Language)


def test_get_primary_translations():
    r = isle.get_primary_translations()
    assert isinstance(r, list)
    assert isinstance(r[0], str)


def test_get_timezones():
    r = isle.get_timezones()
    assert isinstance(r, list)
    assert isinstance(r[0], dict)
    assert "zones" in r[0]
