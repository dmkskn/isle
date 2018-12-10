import unittest

from themoviedb.objects.company import Company
from themoviedb.objects.others import Country, Image


class CompanyTestCase(unittest.TestCase):
    def setUp(self):
        self.company_id = 1
        self.company = Company(self.company_id)

    def test_repr(self):
        self.assertEqual(self.company.__repr__(), f"Company({self.company_id})")

    def test_name_attr(self):
        self.assertIsInstance(self.company.name, str)

    def test_also_known_as_attr(self):
        self.assertIsInstance(self.company.also_known_as, list)

    def test_description_attr(self):
        self.assertIsInstance(self.company.description, str)

    def test_homepage_attr(self):
        self.assertIsInstance(self.company.homepage, str)

    def test_country_attr(self):
        self.assertIsInstance(self.company.country, (Country, type(None)))

    def test_parent_company_attr(self):
        self.assertIsInstance(self.company.parent_company, (str, type(None)))

    def test_logos_attr(self):
        self.assertIsInstance(self.company.logos, list)
        self.assertIsInstance(self.company.logos[0], Image)

    def test_get_details(self):
        details = self.company.get_details()
        self.assertDictEqual(details, self.company.data)

    def test_get_alternative_names(self):
        names = self.company.get_alternative_names()
        self.assertDictEqual(names, self.company.data["alternative_names"])

    def test_get_images(self):
        images = self.company.get_images()
        self.assertDictEqual(images, self.company.data["images"])


if __name__ == "__main__":
    unittest.main()
