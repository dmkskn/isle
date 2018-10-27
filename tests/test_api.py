import os
import json
import inspect
import unittest
from urllib.parse import urlencode
from urllib.request import urlopen

import themoviedb as tmdb


class SearchMovieTestCase(unittest.TestCase):
    BASEURL = "https://api.themoviedb.org/3/search/movie?"

    @classmethod
    def setUpClass(cls):
        cls.movie_title = "harry potter"
        cls.results = tmdb.search_movie(cls.movie_title)
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
        self.assertIsInstance(self.results_list[0], tmdb.Movie)

    def test_title_is_required(self):
        kwargs = {"year": 1953}
        self.assertRaises(TypeError, tmdb.search_movie, **kwargs)

    def test_all_args_except_the_first_one_are_kwargs(self):
        args = (self.movie_title, 1953)
        self.assertRaises(TypeError, tmdb.search_movie, *args)

    def test_amount_of_results(self):
        self.assertEqual(len(self.results_list), self.total_results)

    def test_preloaded_attr(self):
        gen = tmdb.search_movie(self.movie_title, preload=False)
        movie = next(gen)
        self.assertSetEqual(set(movie.data.keys()), {"id"})

        gen = tmdb.search_movie(self.movie_title, preload=True)
        movie = next(gen)
        self.assertIn("original_title", movie.data.keys())
        self.assertIn("alternative_titles", movie.data.keys())
        self.assertIn("credits", movie.data.keys())
        self.assertIn("changes", movie.data.keys())
        # and so on


class SearchShowTestCase(unittest.TestCase):
    BASEURL = "https://api.themoviedb.org/3/search/tv?"

    @classmethod
    def setUpClass(cls):
        cls.show_name = "lost"
        cls.results = tmdb.search_show(cls.show_name)
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
        self.assertIsInstance(self.results_list[0], tmdb.Show)

    def test_query_is_required(self):
        kwargs = {"first_air_date_year": 2004}
        self.assertRaises(TypeError, tmdb.search_show, **kwargs)

    def test_all_args_except_the_first_one_are_kwargs(self):
        args = (self.show_name, 2004)
        self.assertRaises(TypeError, tmdb.search_show, *args)

    def test_amount_of_results(self):
        self.assertEqual(len(self.results_list), self.total_results)

    def test_preloaded_attr(self):
        gen = tmdb.search_show(self.show_name, preload=False)
        show = next(gen)
        self.assertSetEqual(set(show.data.keys()), {"id"})

        gen = tmdb.search_show(self.show_name, preload=True)
        show = next(gen)
        self.assertIn("original_name", show.data.keys())
        self.assertIn("alternative_titles", show.data.keys())
        self.assertIn("screened_theatrically", show.data.keys())
        self.assertIn("external_ids", show.data.keys())
        # and so on


class SearchPersonTestCase(unittest.TestCase):
    BASEURL = "https://api.themoviedb.org/3/search/person?"

    @classmethod
    def setUpClass(cls):
        cls.person_name = "Abrams"
        cls.results = tmdb.search_person(cls.person_name)
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
        self.assertIsInstance(self.results_list[0], tmdb.Person)

    def test_query_is_required(self):
        kwargs = {"language": "en-US"}
        self.assertRaises(TypeError, tmdb.search_person, **kwargs)

    def test_all_args_except_the_first_one_are_kwargs(self):
        args = (self.person_name, True)
        self.assertRaises(TypeError, tmdb.search_person, *args)

    def test_amount_of_results(self):
        self.assertEqual(len(self.results_list), self.total_results)

    def test_preloaded_attr(self):
        gen = tmdb.search_person(self.person_name, preload=False)
        person = next(gen)
        self.assertSetEqual(set(person.data.keys()), {"id"})

        gen = tmdb.search_person(self.person_name, preload=True)
        person = next(gen)
        self.assertIn("name", person.data.keys())
        self.assertIn("movie_credits", person.data.keys())
        self.assertIn("tv_credits", person.data.keys())
        self.assertIn("also_known_as", person.data.keys())
        # and so on


class SearchCompanyTestCase(unittest.TestCase):
    BASEURL = "https://api.themoviedb.org/3/search/company?"

    @classmethod
    def setUpClass(cls):
        cls.company_name = "Sony"
        cls.results = tmdb.search_company(cls.company_name)
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
        self.assertIsInstance(self.results_list[0], tmdb.Company)

    def test_query_is_required(self):
        self.assertRaises(TypeError, tmdb.search_company)

    def test_amount_of_results(self):
        self.assertEqual(len(self.results_list), self.total_results)

    def test_preloaded_attr(self):
        gen = tmdb.search_company(self.company_name, preload=False)
        company = next(gen)
        self.assertSetEqual(set(company.data.keys()), {"id"})

        gen = tmdb.search_company(self.company_name, preload=True)
        company = next(gen)
        self.assertIn("name", company.data.keys())
        self.assertIn("origin_country", company.data.keys())
        self.assertIn("parent_company", company.data.keys())
        # and so on


class DiscoverMovieTestCase(unittest.TestCase):
    BASEURL = "https://api.themoviedb.org/3/discover/movie?"

    @classmethod
    def setUpClass(cls):
        cls.options = {
            "sort_by": "popularity.desc",
            "with_crew": 488,  # Steven Spielberg
            "with_cast": 3,  # Harrison Ford
        }
        cls.results = tmdb.discover_movies(cls.options)
        cls.results_list = list(cls.results)
        cls.api_response = cls.get_api_response(cls.options)
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
        self.assertIsInstance(self.results_list[0], tmdb.Movie)

    def test_amount_of_results(self):
        self.assertEqual(len(self.results_list), self.total_results)

    def test_preloaded_attr(self):
        gen = tmdb.discover_movies(self.options, preload=False)
        movie = next(gen)
        self.assertSetEqual(set(movie.data.keys()), {"id"})

        gen = tmdb.discover_movies(self.options, preload=False)
        movie = next(gen)
        self.assertIn("original_title", movie.data.keys())
        self.assertIn("alternative_titles", movie.data.keys())
        self.assertIn("credits", movie.data.keys())
        self.assertIn("changes", movie.data.keys())
        # and so on


class DiscoverShowTestCase(unittest.TestCase):
    BASEURL = "https://api.themoviedb.org/3/discover/tv?"

    @classmethod
    def setUpClass(cls):
        cls.options = {
            "sort_by": "popularity.desc",
            "with_companies": 278,  # Propaganda Films
        }
        cls.results = tmdb.discover_shows(cls.options)
        cls.results_list = list(cls.results)
        cls.api_response = cls.get_api_response(cls.options)
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
        self.assertIsInstance(self.results_list[0], tmdb.Show)

    def test_amount_of_results(self):
        self.assertEqual(len(self.results_list), self.total_results)

    def test_preloaded_attr(self):
        gen = tmdb.discover_shows(self.options, preload=False)
        show = next(gen)
        self.assertSetEqual(set(show.data.keys()), {"id"})

        gen = tmdb.discover_shows(self.options, preload=True)
        show = next(gen)
        self.assertIn("original_name", show.data.keys())
        self.assertIn("alternative_titles", show.data.keys())
        self.assertIn("screened_theatrically", show.data.keys())
        self.assertIn("external_ids", show.data.keys())
        # and so on


class GetCertificationsTestCase(unittest.TestCase):
    def test_get_movie_certifications(self):
        res = tmdb.get_movie_certifications()
        self.assertIsInstance(res, dict)
        self.assertNotIn("certifications", res)
        self.assertIn("US", res)
        self.assertIsInstance(res["US"], list)

    def test_get_show_certifications(self):
        res = tmdb.get_show_certifications()
        self.assertIsInstance(res, dict)
        self.assertNotIn("certifications", res)
        self.assertIn("US", res)
        self.assertIsInstance(res["US"], list)


class GetGenresTestCase(unittest.TestCase):
    def test_get_movie_genres(self):
        res = tmdb.get_movie_genres()
        self.assertIsInstance(res, list)

    def test_get_show_genres(self):
        res = tmdb.get_show_genres()
        self.assertIsInstance(res, list)


class GetConfigurationsTestCase(unittest.TestCase):
    def test_get_image_configurations(self):
        res = tmdb.get_image_configurations()
        self.assertIsInstance(res, dict)
        self.assertIn("images", res)
        self.assertIn("base_url", res["images"])

    def test_get_countries(self):
        res = tmdb.get_countries()
        self.assertIsInstance(res, list)
        self.assertIn("english_name", res[0])

    def test_get_jobs(self):
        res = tmdb.get_jobs()
        self.assertIsInstance(res, list)
        self.assertIsInstance(res[0], dict)
        self.assertIn("department", res[0])

    def test_get_languages(self):
        res = tmdb.get_languages()
        self.assertIsInstance(res, list)
        self.assertIsInstance(res[0], dict)
        self.assertIn("english_name", res[0])
        self.assertIn("iso_639_1", res[0])
        self.assertIn("name", res[0])

    def test_get_primary_translations(self):
        res = tmdb.get_primary_translations()
        self.assertIsInstance(res, list)
        self.assertIsInstance(res[0], str)

    def test_get_timezones(self):
        res = tmdb.get_timezones()
        self.assertIsInstance(res, list)
        self.assertIsInstance(res[0], dict)
        self.assertIn("zones", res[0])


if __name__ == "__main__":
    unittest.main()
