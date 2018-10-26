import unittest
import inspect
from themoviedb._objects import _BaseTMDbObject, Movie, Show, Person, Company, Keyword


class BaseTMDbObjectTestCase(unittest.TestCase):
    def setUp(self):
        self.movie_id = 18148
        _BaseTMDbObject.__abstractmethods__ = frozenset()
        self.base = _BaseTMDbObject(self.movie_id)  # pylint: disable=E0110

    def test_request(self):
        url = f"https://api.themoviedb.org/3/movie/{self.movie_id}"
        params = {}
        res = self.base._request(url, **params)
        self.assertEqual(res["original_title"], "東京物語")

    def test_iter_request(self):
        url = f"https://api.themoviedb.org/3/movie/{self.movie_id}/reviews"
        params = {}
        res = self.base._iter_request(url, **params)
        item = next(res)
        self.assertTrue(inspect.isgenerator(res))
        self.assertIsInstance(item, dict)


class MovieTestCase(unittest.TestCase):
    def setUp(self):
        self.movie_id = 18148
        self.changed_movie = Movie(self.movie_id, preload=False)
        self.not_changed_movie = Movie(self.movie_id, preload=False)
        self.preloaded_movie = Movie(self.movie_id, preload=True)

    def test_raise_error_when_init_without_id(self):
        with self.assertRaises(TypeError):
            _ = Movie() # pylint: disable=E1120

    def test_preloaded(self):
        movie = Movie(self.movie_id)
        self.assertDictEqual(self.preloaded_movie.data, movie.get_all())

    def test_get_details(self):
        details = self.changed_movie.get_details()
        self.assertDictEqual(details, self.changed_movie.data)

    def test_get_alternative_titles(self):
        alternative_titles = self.changed_movie.get_alternative_titles()
        self.assertDictEqual(
            alternative_titles, self.changed_movie.data["alternative_titles"]
        )

    def test_get_changes(self):
        changes = self.changed_movie.get_changes()
        self.assertDictEqual(changes, self.changed_movie.data["changes"])

    def test_get_credits(self):
        credits = self.changed_movie.get_credits()
        self.assertDictEqual(credits, self.changed_movie.data["credits"])

    def test_get_external_ids(self):
        external_ids = self.changed_movie.get_external_ids()
        self.assertDictEqual(external_ids, self.changed_movie.data["external_ids"])

    def test_get_images(self):
        images = self.changed_movie.get_images()
        self.assertDictEqual(images, self.changed_movie.data["images"])

    def test_get_keywords(self):
        keywords = self.changed_movie.get_keywords()
        self.assertDictEqual(keywords, self.changed_movie.data["keywords"])

    def test_get_release_dates(self):
        release_dates = self.changed_movie.get_release_dates()
        self.assertDictEqual(release_dates, self.changed_movie.data["release_dates"])

    def test_get_videos(self):
        videos = self.changed_movie.get_videos()
        self.assertIsInstance(videos, dict)
        self.assertDictEqual(videos, self.changed_movie.data["videos"])

    def test_get_translations(self):
        translations = self.changed_movie.get_translations()
        self.assertDictEqual(translations, self.changed_movie.data["translations"])

    def test_iter_recommendations(self):
        gen = self.changed_movie.iter_recommendations()
        item = next(gen)
        self.assertTrue(inspect.isgenerator(gen))
        self.assertIsInstance(item, dict)
        self.assertNotEqual(item["id"], self.changed_movie.tmdb_id)

    def test_iter_similar_movies(self):
        gen = self.changed_movie.iter_similar_movies()
        item = next(gen)
        self.assertTrue(inspect.isgenerator(gen))
        self.assertIsInstance(item, dict)
        self.assertNotEqual(item["id"], self.changed_movie.tmdb_id)

    def test_iter_reviews(self):
        gen = self.changed_movie.iter_reviews()
        item = next(gen)
        self.assertTrue(inspect.isgenerator(gen))
        self.assertIsInstance(item, dict)
        self.assertIn("author", item)
        self.assertIn("content", item)

    def test_iter_lists(self):
        gen = self.changed_movie.iter_lists()
        item = next(gen)
        self.assertTrue(inspect.isgenerator(gen))
        self.assertIsInstance(item, dict)
        self.assertIn("description", item)
        self.assertIn("item_count", item)


class ShowTestCase(unittest.TestCase):
    def setUp(self):
        self.show_id = 1399
        self.changed_show = Show(self.show_id, preload=False)
        self.not_changed_show = Show(self.show_id, preload=False)
        self.preloaded_show = Show(self.show_id, preload=True)

    def test_raise_error_when_init_without_id(self):
        with self.assertRaises(TypeError):
            _ = Show() # pylint: disable=E1120

    def test_preloaded(self):
        show = Show(self.show_id)
        self.assertDictEqual(self.preloaded_show.data, show.get_all())

    def test_get_details(self):
        details = self.changed_show.get_details()
        self.assertDictEqual(details, self.changed_show.data)

    def test_get_alternative_titles(self):
        alternative_titles = self.changed_show.get_alternative_titles()
        self.assertDictEqual(
            alternative_titles, self.changed_show.data["alternative_titles"]
        )

    def test_get_changes(self):
        changes = self.changed_show.get_changes()
        self.assertDictEqual(changes, self.changed_show.data["changes"])

    def test_get_content_ratings(self):
        content_ratings = self.changed_show.get_content_ratings()
        self.assertDictEqual(content_ratings, self.changed_show.data["content_ratings"])

    def test_get_credits(self):
        credits = self.changed_show.get_credits()
        self.assertDictEqual(credits, self.changed_show.data["credits"])

    def test_get_episode_groups(self):
        episode_groups = self.changed_show.get_episode_groups()
        self.assertDictEqual(episode_groups, self.changed_show.data["episode_groups"])

    def test_get_external_ids(self):
        external_ids = self.changed_show.get_external_ids()
        self.assertDictEqual(external_ids, self.changed_show.data["external_ids"])

    def test_get_images(self):
        images = self.changed_show.get_images()
        self.assertDictEqual(images, self.changed_show.data["images"])

    def test_get_keywords(self):
        keywords = self.changed_show.get_keywords()
        self.assertDictEqual(keywords, self.changed_show.data["keywords"])

    def test_iter_recommendations(self):
        gen = self.changed_show.iter_recommendations()
        item = next(gen)
        self.assertTrue(inspect.isgenerator(gen))
        self.assertIsInstance(item, dict)
        self.assertNotEqual(item["id"], self.changed_show.tmdb_id)

    def test_iter_reviews(self):
        gen = self.changed_show.iter_reviews()
        item = next(gen)
        self.assertTrue(inspect.isgenerator(gen))
        self.assertIsInstance(item, dict)
        self.assertIn("author", item)
        self.assertIn("content", item)

    def test_get_screened_theatrically(self):
        screened_theatrically = self.changed_show.get_screened_theatrically()
        self.assertDictEqual(
            screened_theatrically, self.changed_show.data["screened_theatrically"]
        )

    def test_iter_similar_shows(self):
        gen = self.changed_show.iter_similar_shows()
        item = next(gen)
        self.assertTrue(inspect.isgenerator(gen))
        self.assertIsInstance(item, dict)
        self.assertNotEqual(item["id"], self.changed_show.tmdb_id)

    def test_get_translations(self):
        translations = self.changed_show.get_translations()
        self.assertDictEqual(translations, self.changed_show.data["translations"])

    def test_get_videos(self):
        videos = self.changed_show.get_videos()
        self.assertDictEqual(videos, self.changed_show.data["videos"])


class PersonTestCase(unittest.TestCase):
    def setUp(self):
        self.person_id = 287
        self.changed_person = Person(self.person_id, preload=False)
        self.not_changed_person = Person(self.person_id, preload=False)
        self.preloaded_person = Person(self.person_id, preload=True)

    def test_preloaded(self):
        person = Person(self.person_id)
        self.assertDictEqual(self.preloaded_person.data, person.get_all())

    def test_get_details(self):
        details = self.changed_person.get_details()
        self.assertDictEqual(details, self.changed_person.data)

    def test_get_changes(self):
        changes = self.changed_person.get_changes()
        self.assertDictEqual(changes, self.changed_person.data["changes"])

    def test_get_movie_credits(self):
        credits = self.changed_person.get_movie_credits()
        self.assertDictEqual(credits, self.changed_person.data["movie_credits"])

    def test_get_show_credits(self):
        credits = self.changed_person.get_show_credits()
        self.assertDictEqual(credits, self.changed_person.data["tv_credits"])

    def test_get_combined_credits(self):
        # Get the movie and TV credits together in a single response.
        credits = self.changed_person.get_combined_credits()
        self.assertDictEqual(credits, self.changed_person.data["combined_credits"])

    def test_get_external_ids(self):
        external_ids = self.changed_person.get_external_ids()
        self.assertDictEqual(external_ids, self.changed_person.data["external_ids"])

    def test_get_images(self):
        images = self.changed_person.get_images()
        self.assertDictEqual(images, self.changed_person.data["images"])

    def test_iter_tagged_images(self):
        gen = self.changed_person.iter_tagged_images()
        item = next(gen)
        self.assertTrue(inspect.isgenerator(gen))
        self.assertIsInstance(item, dict)
        self.assertIn("file_path", item)
        self.assertIn("height", item)
        self.assertIn("width", item)

    def test_get_translations(self):
        translations = self.changed_person.get_translations()
        self.assertDictEqual(translations, self.changed_person.data["translations"])


class CompanyTestCase(unittest.TestCase):
    def setUp(self):
        self.company_id = 1
        self.changed_company = Company(self.company_id, preload=True)
        self.not_changed_company = Company(self.company_id, preload=False)

    def test_get_details(self):
        details = self.changed_company.get_details()
        self.assertDictEqual(details, self.changed_company.data)

    def test_get_alternative_names(self):
        alternative_names = self.changed_company.get_alternative_names()
        self.assertDictEqual(
            alternative_names, self.changed_company.data["alternative_names"]
        )

    def test_get_images(self):
        images = self.changed_company.get_images()
        self.assertDictEqual(images, self.changed_company.data["images"])


class KeywordTestCase(unittest.TestCase):
    def setUp(self):
        self.keyword_id = 3417
        self.keyword_name = "wormhole"
        self.keyword = Keyword(self.keyword_id)._with_name(self.keyword_name)

    def test_init_keyword(self):
        self.assertEqual(self.keyword.tmdb_id, self.keyword_id)
        self.assertDictEqual(
            self.keyword.data, {"id": self.keyword_id, "name": self.keyword_name}
        )

    def test_iter_movies(self):
        res = self.keyword.iter_movies()
        item = next(res)
        self.assertTrue(inspect.isgenerator(res))
        self.assertIsInstance(item, Movie)

    def test_keyword_to_str(self):
        self.assertEqual(str(self.keyword), self.keyword_name)


if __name__ == "__main__":
    unittest.main()
