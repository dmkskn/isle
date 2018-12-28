import pytest

from isle import Company
from isle.objects import Country, Image


COMPANY_ID = 1


@pytest.fixture
def empty_company():
    company = Company(COMPANY_ID)
    assert company.data.keys() == {"id"}
    return company


@pytest.fixture(scope="module")
def company():
    company = Company(COMPANY_ID)
    assert company.data.keys() == {"id"}
    company._init()
    assert company.data.keys() != {"id"}
    return company


def test_name_attr(company: Company):
    assert isinstance(company.name, str)
    assert company.name == company.data["name"]


def test_also_known_as_attr(company: Company):
    assert isinstance(company.also_known_as, list)


def test_description_attr(company: Company):
    assert isinstance(company.description, str)
    assert company.description == company.data["description"]


def test_homepage_attr(company: Company):
    assert isinstance(company.homepage, str)
    assert company.homepage == company.data["homepage"]


def test_country_attr(company: Company):
    assert isinstance(company.country, (Country, type(None)))


def test_parent_company_attr(company: Company):
    assert isinstance(company.parent_company, (str, type(None)))


def test_logos_attr(company: Company):
    assert isinstance(company.logos, list)
    assert all(isinstance(item, Image) for item in company.logos)


def test_get_details(empty_company: Company):
    details = empty_company.get_details()
    assert details == empty_company.data


def test_get_alternative_names(empty_company: Company):
    names = empty_company.get_alternative_names()
    assert names == empty_company.data["alternative_names"]


def test_get_images(empty_company: Company):
    images = empty_company.get_images()
    assert images == empty_company.data["images"]


def test_eq():
    assert Company(1) == Company(1)


def test_not_eq():
    assert Company(1) != Company(10)
