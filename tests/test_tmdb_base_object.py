import unittest
import inspect

from themoviedb.objects._tmdb import TMDb


class TMDbTestCase(unittest.TestCase):
    def setUp(self):
        self.movie_id = 18148
        TMDb.__abstractmethods__ = frozenset()
        self.base = TMDb(self.movie_id)  # pylint: disable=E0110

    def test_request(self):
        url = f"https://api.themoviedb.org/3/movie/{self.movie_id}"
        params = {}
        self.assertEqual(self.base.n_requests, 0)
        res = self.base._request(url, **params)
        self.assertEqual(res["original_title"], "東京物語")
        self.assertEqual(self.base.n_requests, 1)

    def test_iter_request(self):
        url = f"https://api.themoviedb.org/3/movie/{self.movie_id}/reviews"
        params = {}
        self.assertEqual(self.base.n_requests, 0)
        res = self.base._iter_request(url, **params)
        item = next(res)
        self.assertTrue(inspect.isgenerator(res))
        self.assertIsInstance(item, dict)
        self.assertEqual(self.base.n_requests, 1)

    def test_n_requests(self):
        url_1 = f"https://api.themoviedb.org/3/movie/{self.movie_id}"
        url_2 = f"https://api.themoviedb.org/3/movie/{self.movie_id}/reviews"
        params = {}
        self.assertEqual(self.base.n_requests, 0)
        self.base._request(url_1, **params)
        self.assertEqual(self.base.n_requests, 1)
        self.base._request(url_1, **params)
        self.assertEqual(self.base.n_requests, 2)
        self.base._request(url_1, **params)
        self.assertEqual(self.base.n_requests, 3)
        self.base._iter_request(url_2, **params)
        self.assertEqual(self.base.n_requests, 4)


if __name__ == "__main__":
    unittest.main()
