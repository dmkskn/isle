import os
import json
import inspect
import unittest
from urllib.parse import urlencode
from urllib.request import urlopen

import src


class TMDbAPITestCase(unittest.TestCase):
    pass



class SearchMovieTestCase(unittest.TestCase):
    BASEURL = "https://api.themoviedb.org/3/search/movie?"

    @classmethod
    def setUpClass(cls):
        cls.movie_title = "harry potter"
        cls.results = src.search_movie(cls.movie_title)
        cls.results_list = list(cls.results)
        params = {
            "api_key": os.environ["TMDB_API_KEY"],
            "language": "en-US",
            "include_adult": "false",
            "query": cls.movie_title,
        }
        response = cls.get_api_response(**params, page=1)
        cls.total_pages = response["total_pages"]
        cls.total_results = response["total_results"]
        cls.api_response_movies = []
        for page in range(1, cls.total_pages + 1):
            results = cls.get_api_response(**params, page=page)["results"]
            for movie in results:
                cls.api_response_movies.append(movie)

    @classmethod
    def get_api_response(cls, **params):
        params = urlencode(params)
        response = urlopen(f"{cls.BASEURL}{params}")
        return json.loads(response.read().decode("utf-8"))

    def test_output_is_generator(self):
        self.assertTrue(inspect.isgenerator(self.results))

    def test_output_item_is_Movie_instance(self):
        self.assertIsInstance(self.results_list[0], src.Movie)

    def test_title_is_required(self):
        kwargs = {"year": 1953}
        self.assertRaises(TypeError, src.search_movie, **kwargs)

    def test_all_args_except_the_first_one_are_kwargs(self):
        args = (self.movie_title, 1953)
        self.assertRaises(TypeError, src.search_movie, *args)

    def test_amount_of_results(self):
        self.assertEqual(len(self.results_list), self.total_results)

    def test_api_response_and_search_movie_response_are_the_same(self):
        api_response_tmdb_ids = {m["id"] for m in self.api_response_movies}
        search_movie_tmdb_ids = {m.tmdb_id for m in self.results_list}
        self.assertSetEqual(api_response_tmdb_ids, search_movie_tmdb_ids)



class SearchShowTestCase(unittest.TestCase):
    pass



class SearchPersonTestCase(unittest.TestCase):
    pass



class SearchCompanyTestCase(unittest.TestCase):
    pass



class DiscoverMovieTestCase(unittest.TestCase):
    pass



class DiscoverShowTestCase(unittest.TestCase):
    pass



class DiscoverPersonTestCase(unittest.TestCase):
    pass



if __name__ == "__main__":
    unittest.main()
