import os
import json
import inspect
import unittest
from urllib.parse import urlencode
from urllib.request import urlopen

import src


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


class SearchShowTestCase(unittest.TestCase):
    BASEURL = "https://api.themoviedb.org/3/search/tv?"

    @classmethod
    def setUpClass(cls):
        cls.show_name = "lost"
        cls.results = src.search_show(cls.show_name)
        cls.results_list = list(cls.results)
        params = {
            "api_key": os.environ["TMDB_API_KEY"],
            "language": "en-US",
            "query": cls.show_name,
        }
        response = cls.get_api_response(**params, page=1)
        cls.total_pages = response["total_pages"]
        cls.total_results = response["total_results"]
        cls.api_response_shows = []
        for page in range(1, cls.total_pages + 1):
            results = cls.get_api_response(**params, page=page)["results"]
            for movie in results:
                cls.api_response_shows.append(movie)

    @classmethod
    def get_api_response(cls, **params):
        params = urlencode(params)
        response = urlopen(f"{cls.BASEURL}{params}")
        return json.loads(response.read().decode("utf-8"))

    def test_output_is_generator(self):
        self.assertTrue(inspect.isgenerator(self.results))

    def test_output_item_is_Show_instance(self):
        self.assertIsInstance(self.results_list[0], src.Show)

    def test_query_is_required(self):
        kwargs = {"first_air_date_year": 2004}
        self.assertRaises(TypeError, src.search_show, **kwargs)

    def test_all_args_except_the_first_one_are_kwargs(self):
        args = (self.show_name, 2004)
        self.assertRaises(TypeError, src.search_show, *args)

    def test_amount_of_results(self):
        self.assertEqual(len(self.results_list), self.total_results)


class SearchPersonTestCase(unittest.TestCase):
    BASEURL = "https://api.themoviedb.org/3/search/person?"

    @classmethod
    def setUpClass(cls):
        cls.person_name = "Abrams"
        cls.results = src.search_person(cls.person_name)
        cls.results_list = list(cls.results)
        params = {
            "api_key": os.environ["TMDB_API_KEY"],
            "language": "en-US",
            "include_adult": "false",
            "query": cls.person_name,
        }
        response = cls.get_api_response(**params, page=1)
        cls.total_pages = response["total_pages"]
        cls.total_results = response["total_results"]
        cls.api_response_people = []
        for page in range(1, cls.total_pages + 1):
            results = cls.get_api_response(**params, page=page)["results"]
            for movie in results:
                cls.api_response_people.append(movie)

    @classmethod
    def get_api_response(cls, **params):
        params = urlencode(params)
        response = urlopen(f"{cls.BASEURL}{params}")
        return json.loads(response.read().decode("utf-8"))

    def test_output_is_generator(self):
        self.assertTrue(inspect.isgenerator(self.results))

    def test_output_item_is_Person_instance(self):
        self.assertIsInstance(self.results_list[0], src.Person)

    def test_query_is_required(self):
        kwargs = {"language": "en-US"}
        self.assertRaises(TypeError, src.search_person, **kwargs)

    def test_all_args_except_the_first_one_are_kwargs(self):
        args = (self.person_name, True)
        self.assertRaises(TypeError, src.search_person, *args)

    def test_amount_of_results(self):
        self.assertEqual(len(self.results_list), self.total_results)


class SearchCompanyTestCase(unittest.TestCase):
    BASEURL = "https://api.themoviedb.org/3/search/company?"

    @classmethod
    def setUpClass(cls):
        cls.company_name = "Sony"
        cls.results = src.search_company(cls.company_name)
        cls.results_list = list(cls.results)
        params = {"api_key": os.environ["TMDB_API_KEY"], "query": cls.company_name}
        response = cls.get_api_response(**params, page=1)
        cls.total_pages = response["total_pages"]
        cls.total_results = response["total_results"]
        cls.api_response_companies = []
        for page in range(1, cls.total_pages + 1):
            results = cls.get_api_response(**params, page=page)["results"]
            for movie in results:
                cls.api_response_companies.append(movie)

    @classmethod
    def get_api_response(cls, **params):
        params = urlencode(params)
        response = urlopen(f"{cls.BASEURL}{params}")
        return json.loads(response.read().decode("utf-8"))

    def test_output_is_generator(self):
        self.assertTrue(inspect.isgenerator(self.results))

    def test_output_item_is_Company_instance(self):
        self.assertIsInstance(self.results_list[0], src.Company)

    def test_query_is_required(self):
        self.assertRaises(TypeError, src.search_company)

    def test_amount_of_results(self):
        self.assertEqual(len(self.results_list), self.total_results)


class DiscoverMovieTestCase(unittest.TestCase):
    BASEURL = "https://api.themoviedb.org/3/discover/movie?"

    @classmethod
    def setUpClass(cls):
        options = {
            "sort_by": "popularity.desc",
            "with_crew": 488,  # Steven Spielberg
            "with_cast": 3,  # Harrison Ford
        }
        cls.results = src.discover_movies(options)
        cls.results_list = list(cls.results)
        cls.api_response = cls.get_api_response(options)
        cls.total_results = cls.api_response["total_results"]

    @classmethod
    def get_api_response(cls, options):
        params = {"api_key": os.environ["TMDB_API_KEY"], **options}
        params = urlencode(params)
        response = urlopen(f"{cls.BASEURL}{params}")
        return json.loads(response.read().decode("utf-8"))

    def test_output_is_generator(self):
        self.assertTrue(inspect.isgenerator(self.results))

    def test_output_item_is_Movie_instance(self):
        self.assertIsInstance(self.results_list[0], src.Movie)

    def test_amount_of_results(self):
        self.assertEqual(len(self.results_list), self.total_results)


class DiscoverShowTestCase(unittest.TestCase):
    BASEURL = "https://api.themoviedb.org/3/discover/tv?"

    @classmethod
    def setUpClass(cls):
        options = {
            "sort_by": "popularity.desc",
            "with_companies": 278,  # Propaganda Films
        }
        cls.results = src.discover_shows(options)
        cls.results_list = list(cls.results)
        cls.api_response = cls.get_api_response(options)
        cls.total_results = cls.api_response["total_results"]

    @classmethod
    def get_api_response(cls, options):
        params = {"api_key": os.environ["TMDB_API_KEY"], **options}
        params = urlencode(params)
        response = urlopen(f"{cls.BASEURL}{params}")
        return json.loads(response.read().decode("utf-8"))

    def test_output_is_generator(self):
        self.assertTrue(inspect.isgenerator(self.results))

    def test_output_item_is_Show_instance(self):
        self.assertIsInstance(self.results_list[0], src.Show)

    def test_amount_of_results(self):
        self.assertEqual(len(self.results_list), self.total_results)


if __name__ == "__main__":
    unittest.main()
