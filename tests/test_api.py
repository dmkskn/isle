import os
import json
import inspect
import unittest
from urllib.parse import urlencode
from urllib.request import urlopen

import themoviedb as tmdb
from themoviedb._objects import Genre, Country, Language


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


class FindTestCase(unittest.TestCase):
    BASEURL = "https://api.themoviedb.org/3/find/{}?"

    def setUp(self):
        self.movie_imdb_id = "tt0046438"
        self.show_imdb_id = "tt4574334"
        self.person_imdb_id = "nm0000093"
        self.episode_tvdb_id = 5_468_124
        self.season_tvdb_id = 651_264

    def test_find_movie(self):
        results = tmdb.find(self.movie_imdb_id, src="imdb_id")
        self.assertEqual(len(results["movie_results"]), 1)
        self.assertIsInstance(results["movie_results"][0], tmdb._objects.Movie)
        self.assertEqual(results["movie_results"][0].imdb_id, self.movie_imdb_id)

    def test_find_person(self):
        results = tmdb.find(self.person_imdb_id, src="imdb_id")
        self.assertEqual(len(results["person_results"]), 1)
        self.assertIsInstance(results["person_results"][0], tmdb._objects.Person)
        self.assertEqual(results["person_results"][0].imdb_id, self.person_imdb_id)

    def test_find_show(self):
        results = tmdb.find(self.show_imdb_id, src="imdb_id")
        self.assertEqual(len(results["tv_results"]), 1)
        self.assertIsInstance(results["tv_results"][0], tmdb._objects.Show)
        self.assertEqual(results["tv_results"][0].imdb_id, self.show_imdb_id)

    def test_find_episode(self):
        results = tmdb.find(self.episode_tvdb_id, src="tvdb_id")
        self.assertEqual(len(results["tv_episode_results"]), 1)
        self.assertIsInstance(results["tv_episode_results"][0], tmdb._objects.Episode)
        self.assertEqual(results["tv_episode_results"][0].tvdb_id, self.episode_tvdb_id)

    def test_find_season(self):
        results = tmdb.find(self.season_tvdb_id, src="tvdb_id")
        self.assertEqual(len(results["tv_season_results"]), 1)
        self.assertIsInstance(results["tv_season_results"][0], tmdb._objects.Season)
        self.assertEqual(results["tv_season_results"][0].tvdb_id, self.season_tvdb_id)


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

    def test_get_key(self):
        movie_cert = tmdb.get_movie_certifications("US")
        show_cert = tmdb.get_show_certifications("US")
        self.assertIsInstance(movie_cert, list)
        self.assertIsInstance(show_cert, list)


class GetGenresTestCase(unittest.TestCase):
    def test_get_movie_genres(self):
        res = tmdb.get_movie_genres()
        self.assertIsInstance(res, list)

    def test_get_show_genres(self):
        res = tmdb.get_show_genres()
        self.assertIsInstance(res, list)

    def test_get_genre_objects(self):
        movie_genres = tmdb.get_movie_genres(objects=True)
        show_genres = tmdb.get_show_genres(objects=True)
        self.assertIsInstance(movie_genres[0], Genre)
        self.assertIsInstance(show_genres[0], Genre)


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


class GetCountriesTestCase(unittest.TestCase):
    def test_get_countries(self):
        res = tmdb.get_countries()
        self.assertIsInstance(res, list)
        self.assertIsInstance(res[0], dict)

    def test_get_country_objects(self):
        res = tmdb.get_countries(objects=True)
        self.assertIsInstance(res[0], Country)


class GetLanguagesTestCase(unittest.TestCase):
    def test_get_languages(self):
        res = tmdb.get_languages()
        self.assertIsInstance(res, list)
        self.assertIsInstance(res[0], dict)

    def test_get_language_objects(self):
        res = tmdb.get_languages(objects=True)
        self.assertIsInstance(res[0], Language)


if __name__ == "__main__":
    unittest.main()
