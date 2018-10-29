import os
import json
import inspect
import unittest
from urllib.parse import urlencode
from urllib.request import urlopen

import themoviedb as tmdb


def get_api_response(url, **params):
    params = urlencode(params)
    response = urlopen(f"{url}{params}")
    return json.loads(response.read().decode("utf-8"))


class SearchMovieTestCase(unittest.TestCase):
    BASEURL = "https://api.themoviedb.org/3/search/movie?"

    @classmethod
    def setUpClass(cls):
        cls.title = "harry potter"
        cls.results_genr = tmdb.search_movie(cls.title)
        cls.results_list = list(cls.results_genr)
        cls.n_pages, cls.n_results = cls.get_totals()

    @classmethod
    def get_totals(cls):
        params = {
            "api_key": os.environ["TMDB_API_KEY"],
            "language": "en-US",
            "include_adult": "false",
            "query": cls.title,
            "page": 1,
        }
        response = get_api_response(cls.BASEURL, **params)
        return response["total_pages"], response["total_results"]

    def test_output_is_generator(self):
        self.assertTrue(inspect.isgenerator(self.results_genr))

    def test_output_item_is_Movie_instance(self):
        self.assertIsInstance(self.results_list[0], tmdb.Movie)

    def test_title_is_required(self):
        with self.assertRaises(TypeError):
            tmdb.search_movie(**{"year": 1953})

    def test_all_args_except_the_first_one_are_kwargs(self):
        with self.assertRaises(TypeError):
            tmdb.search_movie(self.title, 1953)

    def test_amount_of_results(self):
        self.assertEqual(len(self.results_list), self.n_results)

    def test_not_preloaded_attr(self):
        movie = next(tmdb.search_movie(self.title, preload=False))
        self.assertSetEqual(set(movie.data.keys()), {"id"})

    def test_preloaded_attr(self):
        movie = next(tmdb.search_movie(self.title, preload=True))
        self.assertIn("original_title", movie.data.keys())
        self.assertIn("alternative_titles", movie.data.keys())
        self.assertIn("credits", movie.data.keys())
        self.assertIn("changes", movie.data.keys())


class SearchShowTestCase(unittest.TestCase):
    BASEURL = "https://api.themoviedb.org/3/search/tv?"

    @classmethod
    def setUpClass(cls):
        cls.name = "lost"
        cls.results_genr = tmdb.search_show(cls.name)
        cls.results_list = list(cls.results_genr)
        cls.n_pages, cls.n_results = cls.get_totals()

    @classmethod
    def get_totals(cls):
        params = {
            "api_key": os.environ["TMDB_API_KEY"],
            "language": "en-US",
            "query": cls.name,
            "page": 1,
        }
        response = get_api_response(cls.BASEURL, **params)
        return response["total_pages"], response["total_results"]

    def test_output_is_generator(self):
        self.assertTrue(inspect.isgenerator(self.results_genr))

    def test_output_item_is_Show_instance(self):
        self.assertIsInstance(self.results_list[0], tmdb.Show)

    def test_query_is_required(self):
        with self.assertRaises(TypeError):
            tmdb.search_show(**{"first_air_date_year": 2004})

    def test_all_args_except_the_first_one_are_kwargs(self):
        with self.assertRaises(TypeError):
            tmdb.search_show(self.name, 2004)

    def test_amount_of_results(self):
        self.assertEqual(len(self.results_list), self.n_results)

    def test_not_preloaded_attr(self):
        show = next(tmdb.search_show(self.name, preload=False))
        self.assertSetEqual(set(show.data.keys()), {"id"})

    def test_preloaded_attr(self):
        show = next(tmdb.search_show(self.name, preload=True))
        self.assertIn("original_name", show.data.keys())
        self.assertIn("alternative_titles", show.data.keys())
        self.assertIn("screened_theatrically", show.data.keys())
        self.assertIn("external_ids", show.data.keys())


class SearchPersonTestCase(unittest.TestCase):
    BASEURL = "https://api.themoviedb.org/3/search/person?"

    @classmethod
    def setUpClass(cls):
        cls.name = "Abrams"
        cls.results_genr = tmdb.search_person(cls.name)
        cls.results_list = list(cls.results_genr)
        cls.n_pages, cls.n_results = cls.get_totals()

    @classmethod
    def get_totals(cls):
        params = {
            "api_key": os.environ["TMDB_API_KEY"],
            "language": "en-US",
            "include_adult": "false",
            "query": cls.name,
            "page": 1,
        }
        response = get_api_response(cls.BASEURL, **params)
        return response["total_pages"], response["total_results"]

    def test_output_is_generator(self):
        self.assertTrue(inspect.isgenerator(self.results_genr))

    def test_output_item_is_Person_instance(self):
        self.assertIsInstance(self.results_list[0], tmdb.Person)

    def test_query_is_required(self):
        with self.assertRaises(TypeError):
            tmdb.search_person(**{"language": "en-US"})

    def test_all_args_except_the_first_one_are_kwargs(self):
        with self.assertRaises(TypeError):
            tmdb.search_person(self.name, True)

    def test_amount_of_results(self):
        self.assertEqual(len(self.results_list), self.n_results)

    def test_not_preloaded_attr(self):
        person = next(tmdb.search_person(self.name, preload=False))
        self.assertSetEqual(set(person.data.keys()), {"id"})

    def test_preloaded_attr(self):
        person = next(tmdb.search_person(self.name, preload=True))
        self.assertIn("name", person.data.keys())
        self.assertIn("movie_credits", person.data.keys())
        self.assertIn("tv_credits", person.data.keys())
        self.assertIn("also_known_as", person.data.keys())


class SearchCompanyTestCase(unittest.TestCase):
    BASEURL = "https://api.themoviedb.org/3/search/company?"

    @classmethod
    def setUpClass(cls):
        cls.name = "Sony"
        cls.results_genr = tmdb.search_company(cls.name)
        cls.results_list = list(cls.results_genr)
        cls.n_pages, cls.n_results = cls.get_totals()

    @classmethod
    def get_totals(cls):
        params = {"api_key": os.environ["TMDB_API_KEY"], "query": cls.name, "page": 1}
        response = get_api_response(cls.BASEURL, **params)
        return response["total_pages"], response["total_results"]

    def test_output_is_generator(self):
        self.assertTrue(inspect.isgenerator(self.results_genr))

    def test_output_item_is_Company_instance(self):
        self.assertIsInstance(self.results_list[0], tmdb.Company)

    def test_query_is_required(self):
        self.assertRaises(TypeError, tmdb.search_company)

    def test_amount_of_results(self):
        self.assertEqual(len(self.results_list), self.n_results)

    def test_not_preloaded_attr(self):
        company = next(tmdb.search_company(self.name, preload=False))
        self.assertSetEqual(set(company.data.keys()), {"id"})

    def test_preloaded_attr(self):
        company = next(tmdb.search_company(self.name, preload=True))
        self.assertIn("name", company.data.keys())
        self.assertIn("origin_country", company.data.keys())
        self.assertIn("parent_company", company.data.keys())


class DiscoverMovieTestCase(unittest.TestCase):
    BASEURL = "https://api.themoviedb.org/3/discover/movie?"

    @classmethod
    def setUpClass(cls):
        cls.options = {
            "sort_by": "popularity.desc",
            "with_crew": 488,  # Steven Spielberg
            "with_cast": 3,  # Harrison Ford
        }
        cls.results_genr = tmdb.discover_movies(cls.options)
        cls.results_list = list(cls.results_genr)
        cls.n_pages, cls.n_results = cls.get_totals()

    @classmethod
    def get_totals(cls):
        params = {"api_key": os.environ["TMDB_API_KEY"], **cls.options}
        response = get_api_response(cls.BASEURL, **params)
        return response["total_pages"], response["total_results"]

    def test_output_is_generator(self):
        self.assertTrue(inspect.isgenerator(self.results_genr))

    def test_output_item_is_Movie_instance(self):
        self.assertIsInstance(self.results_list[0], tmdb.Movie)

    def test_amount_of_results(self):
        self.assertEqual(len(self.results_list), self.n_results)

    def test_not_preloaded_attr(self):
        movie = next(tmdb.discover_movies(self.options, preload=False))
        self.assertSetEqual(set(movie.data.keys()), {"id"})

    def test_preloaded_attr(self):
        movie = next(tmdb.discover_movies(self.options, preload=True))
        self.assertIn("original_title", movie.data.keys())
        self.assertIn("alternative_titles", movie.data.keys())
        self.assertIn("credits", movie.data.keys())
        self.assertIn("changes", movie.data.keys())


class DiscoverShowTestCase(unittest.TestCase):
    BASEURL = "https://api.themoviedb.org/3/discover/tv?"

    @classmethod
    def setUpClass(cls):
        cls.options = {
            "sort_by": "popularity.desc",
            "with_companies": 278,  # Propaganda Films
        }
        cls.results_genr = tmdb.discover_shows(cls.options)
        cls.results_list = list(cls.results_genr)
        cls.n_pages, cls.n_results = cls.get_totals()

    @classmethod
    def get_totals(cls):
        params = {"api_key": os.environ["TMDB_API_KEY"], **cls.options}
        response = get_api_response(cls.BASEURL, **params)
        return response["total_pages"], response["total_results"]

    def test_output_is_generator(self):
        self.assertTrue(inspect.isgenerator(self.results_genr))

    def test_output_item_is_Show_instance(self):
        self.assertIsInstance(self.results_list[0], tmdb.Show)

    def test_amount_of_results(self):
        self.assertEqual(len(self.results_list), self.n_results)

    def test_not_preloaded_attr(self):
        show = next(tmdb.discover_shows(self.options, preload=False))
        self.assertSetEqual(set(show.data.keys()), {"id"})

    def test_preloaded_attr(self):
        show = next(tmdb.discover_shows(self.options, preload=True))
        self.assertIn("original_name", show.data.keys())
        self.assertIn("alternative_titles", show.data.keys())
        self.assertIn("screened_theatrically", show.data.keys())
        self.assertIn("external_ids", show.data.keys())


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
