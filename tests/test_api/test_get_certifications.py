import pytest

import isle


def test_get_movie_certifications():
    r = isle.get_movie_certifications()
    assert isinstance(r, dict)
    assert "US" in r
    assert "certifications" not in r
    assert isinstance(r["US"], list)


def test_get_show_certifications():
    r = isle.get_show_certifications()
    assert isinstance(r, dict)
    assert "US" in r
    assert "certifications" not in r
    assert isinstance(r["US"], list)


def test_get_key():
    movie_cert = isle.get_movie_certifications("US")
    show_cert = isle.get_show_certifications("US")
    assert isinstance(movie_cert, list)
    assert isinstance(show_cert, list)
