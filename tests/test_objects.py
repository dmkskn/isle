import unittest
import inspect
from themoviedb._objects import TMDb, Movie, Show, Person, Company, Keyword, Genre


class TMDbTestCase(unittest.TestCase):
    def setUp(self):
        self.movie_id = 18148
        TMDb.__abstractmethods__ = frozenset()
        self.base = TMDb(self.movie_id)  # pylint: disable=E0110

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
        self.movie = Movie(self.movie_id, preload=False)

    def test_raise_error_when_init_without_id(self):
        with self.assertRaises(TypeError):
            _ = Movie()  # pylint: disable=E1120

    def test_preloaded(self):
        preloaded_movie = Movie(self.movie_id, preload=True)
        data = Movie(self.movie_id).get_all()
        self.assertNotEqual(self.movie.data, data)
        self.assertDictEqual(preloaded_movie.data, data)

    def test_get_details(self):
        details = self.movie.get_details()
        self.assertDictEqual(details, self.movie.data)

    def test_get_alternative_titles(self):
        titles = self.movie.get_alternative_titles()
        self.assertDictEqual(titles, self.movie.data["alternative_titles"])

    def test_get_changes(self):
        changes = self.movie.get_changes()
        self.assertDictEqual(changes, self.movie.data["changes"])

    def test_get_credits(self):
        credits = self.movie.get_credits()
        self.assertDictEqual(credits, self.movie.data["credits"])

    def test_get_external_ids(self):
        external_ids = self.movie.get_external_ids()
        self.assertDictEqual(external_ids, self.movie.data["external_ids"])

    def test_get_images(self):
        images = self.movie.get_images()
        self.assertDictEqual(images, self.movie.data["images"])

    def test_get_keywords(self):
        keywords = self.movie.get_keywords()
        self.assertDictEqual(keywords, self.movie.data["keywords"])

    def test_get_release_dates(self):
        release_dates = self.movie.get_release_dates()
        self.assertDictEqual(release_dates, self.movie.data["release_dates"])

    def test_get_videos(self):
        videos = self.movie.get_videos()
        self.assertIsInstance(videos, dict)
        self.assertDictEqual(videos, self.movie.data["videos"])

    def test_get_translations(self):
        translations = self.movie.get_translations()
        self.assertDictEqual(translations, self.movie.data["translations"])

    def test_iter_recommendations(self):
        recommendations = self.movie.iter_recommendations()
        item = next(recommendations)
        self.assertTrue(inspect.isgenerator(recommendations))
        self.assertIsInstance(item, dict)
        self.assertNotEqual(item["id"], self.movie.tmdb_id)

    def test_iter_similar_movies(self):
        similar_movies = self.movie.iter_similar_movies()
        item = next(similar_movies)
        self.assertTrue(inspect.isgenerator(similar_movies))
        self.assertIsInstance(item, dict)
        self.assertNotEqual(item["id"], self.movie.tmdb_id)

    def test_iter_reviews(self):
        reviews = self.movie.iter_reviews()
        item = next(reviews)
        self.assertTrue(inspect.isgenerator(reviews))
        self.assertIsInstance(item, dict)
        self.assertIn("author", item)
        self.assertIn("content", item)

    def test_iter_lists(self):
        lists = self.movie.iter_lists()
        item = next(lists)
        self.assertTrue(inspect.isgenerator(lists))
        self.assertIsInstance(item, dict)
        self.assertIn("description", item)
        self.assertIn("item_count", item)


class ShowTestCase(unittest.TestCase):
    def setUp(self):
        self.show_id = 1399
        self.show = Show(self.show_id, preload=False)

    def test_raise_error_when_init_without_id(self):
        with self.assertRaises(TypeError):
            _ = Show()  # pylint: disable=E1120

    def test_preloaded(self):
        data = Show(self.show_id).get_all()
        preloaded_show = Show(self.show_id, preload=True)
        self.assertNotEqual(self.show.data, data)
        self.assertDictEqual(preloaded_show.data, data)

    def test_get_details(self):
        details = self.show.get_details()
        self.assertDictEqual(details, self.show.data)

    def test_get_alternative_titles(self):
        titles = self.show.get_alternative_titles()
        self.assertDictEqual(titles, self.show.data["alternative_titles"])

    def test_get_changes(self):
        changes = self.show.get_changes()
        self.assertDictEqual(changes, self.show.data["changes"])

    def test_get_content_ratings(self):
        ratings = self.show.get_content_ratings()
        self.assertDictEqual(ratings, self.show.data["content_ratings"])

    def test_get_credits(self):
        credits = self.show.get_credits()
        self.assertDictEqual(credits, self.show.data["credits"])

    def test_get_episode_groups(self):
        episode_groups = self.show.get_episode_groups()
        self.assertDictEqual(episode_groups, self.show.data["episode_groups"])

    def test_get_external_ids(self):
        external_ids = self.show.get_external_ids()
        self.assertDictEqual(external_ids, self.show.data["external_ids"])

    def test_get_images(self):
        images = self.show.get_images()
        self.assertDictEqual(images, self.show.data["images"])

    def test_get_keywords(self):
        keywords = self.show.get_keywords()
        self.assertDictEqual(keywords, self.show.data["keywords"])

    def test_iter_recommendations(self):
        recommendations = self.show.iter_recommendations()
        item = next(recommendations)
        self.assertTrue(inspect.isgenerator(recommendations))
        self.assertIsInstance(item, dict)
        self.assertNotEqual(item["id"], self.show.tmdb_id)

    def test_iter_reviews(self):
        reviews = self.show.iter_reviews()
        item = next(reviews)
        self.assertTrue(inspect.isgenerator(reviews))
        self.assertIsInstance(item, dict)
        self.assertIn("author", item)
        self.assertIn("content", item)

    def test_get_screened_theatrically(self):
        screened = self.show.get_screened_theatrically()
        self.assertDictEqual(screened, self.show.data["screened_theatrically"])

    def test_iter_similar_shows(self):
        similar_shows = self.show.iter_similar_shows()
        item = next(similar_shows)
        self.assertTrue(inspect.isgenerator(similar_shows))
        self.assertIsInstance(item, dict)
        self.assertNotEqual(item["id"], self.show.tmdb_id)

    def test_get_translations(self):
        translations = self.show.get_translations()
        self.assertDictEqual(translations, self.show.data["translations"])

    def test_get_videos(self):
        videos = self.show.get_videos()
        self.assertDictEqual(videos, self.show.data["videos"])


class PersonTestCase(unittest.TestCase):
    def setUp(self):
        self.person_id = 287
        self.person = Person(self.person_id, preload=False)

    def test_preloaded(self):
        data = Person(self.person_id).get_all()
        preloaded_person = Person(self.person_id, preload=True)
        self.assertNotEqual(self.person.data, data)
        self.assertDictEqual(preloaded_person.data, data)

    def test_get_details(self):
        details = self.person.get_details()
        self.assertDictEqual(details, self.person.data)

    def test_get_changes(self):
        changes = self.person.get_changes()
        self.assertDictEqual(changes, self.person.data["changes"])

    def test_get_movie_credits(self):
        credits = self.person.get_movie_credits()
        self.assertDictEqual(credits, self.person.data["movie_credits"])

    def test_get_show_credits(self):
        credits = self.person.get_show_credits()
        self.assertDictEqual(credits, self.person.data["tv_credits"])

    def test_get_combined_credits(self):
        credits = self.person.get_combined_credits()
        self.assertDictEqual(credits, self.person.data["combined_credits"])

    def test_get_external_ids(self):
        external_ids = self.person.get_external_ids()
        self.assertDictEqual(external_ids, self.person.data["external_ids"])

    def test_get_images(self):
        images = self.person.get_images()
        self.assertDictEqual(images, self.person.data["images"])

    def test_iter_tagged_images(self):
        tagged_images = self.person.iter_tagged_images()
        item = next(tagged_images)
        self.assertTrue(inspect.isgenerator(tagged_images))
        self.assertIsInstance(item, dict)
        self.assertIn("file_path", item)
        self.assertIn("height", item)
        self.assertIn("width", item)

    def test_get_translations(self):
        translations = self.person.get_translations()
        self.assertDictEqual(translations, self.person.data["translations"])


class CompanyTestCase(unittest.TestCase):
    def setUp(self):
        self.company_id = 1
        self.company = Company(self.company_id, preload=True)

    def test_get_details(self):
        details = self.company.get_details()
        self.assertDictEqual(details, self.company.data)

    def test_get_alternative_names(self):
        names = self.company.get_alternative_names()
        self.assertDictEqual(names, self.company.data["alternative_names"])

    def test_get_images(self):
        images = self.company.get_images()
        self.assertDictEqual(images, self.company.data["images"])


class KeywordTestCase(unittest.TestCase):
    def setUp(self):
        self.id_ = 3417
        self.name = "wormhole"
        self.keyword_without_name = Keyword(self.id_, preload=False)
        self.keyword_with_name = Keyword(self.id_, preload=False)._with_name(self.name)

    def test_init_keyword_with_name(self):
        expected_data = {"id": self.id_, "name": self.name}
        self.assertDictEqual(self.keyword_with_name.data, expected_data)

    def test_init_keyword_without_name(self):
        expected_data = {"id": self.id_, "name": self.name}
        self.assertDictEqual(self.keyword_without_name.data, {"id": self.id_})
        self.keyword_without_name.get_details()
        self.assertDictEqual(self.keyword_without_name.data, expected_data)

    def test_iter_movies(self):
        movies = self.keyword_with_name.iter_movies()
        item = next(movies)
        self.assertTrue(inspect.isgenerator(movies))
        self.assertIsInstance(item, Movie)

    def test_keyword_to_str(self):
        self.assertEqual(str(self.keyword_with_name), self.name)
        self.assertEqual(str(self.keyword_without_name), self.name)


class GenreTestCase(unittest.TestCase):
    def setUp(self):
        self.id_ = 12
        self.name = "Adventure"
        self.genre = Genre(self.id_, preload=False)._with_name(self.name)

    def test_init_genre(self):
        expected_data = {"id": self.id_, "name": self.name}
        self.assertDictEqual(self.genre.data, expected_data)

    def test_genre_to_str(self):
        self.assertEqual(str(self.genre), self.name)


if __name__ == "__main__":
    unittest.main()
