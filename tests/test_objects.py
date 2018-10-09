import unittest
from src._objects import _BaseTMDbObject


class BaseTMDbObjectTestCase(unittest.TestCase):
    def setUp(self):
        self.movie_id = 18148
        _BaseTMDbObject.__abstractmethods__ = frozenset()
        self.base = _BaseTMDbObject(id=self.movie_id) # pylint: disable=E0110

    def test_request(self):
        url = f"https://api.themoviedb.org/3/movie/{self.movie_id}"
        params = {}
        res = self.base._request(url, **params)
        self.assertEqual(res["original_title"], "東京物語")

    def test_set_attrs(self):
        attrs = dict.fromkeys(["id", "__is_first_init__", "one", "two"], 1)

        exp_attrs = attrs.keys() - {"id", "__is_first_init__"}
        self.base._set_attrs(**attrs)
        self.assertTrue(
            all([attr in self.base.__dict__.keys() for attr in exp_attrs])
        )
        self.assertTrue(
            all([attr not in self.base.__dict__ for attr in {"id", "__is_first_init__"}])
        )


class MovieTestCase(unittest.TestCase):
    pass


class ShowTestCase(unittest.TestCase):
    pass


class PersonTestCase(unittest.TestCase):
    pass


class CompanyTestCase(unittest.TestCase):
    pass


if __name__ == "__main__":
    unittest.main()
