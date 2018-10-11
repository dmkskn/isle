import unittest
import inspect
from src._objects import _BaseTMDbObject, Movie


class BaseTMDbObjectTestCase(unittest.TestCase):
    def setUp(self):
        self.movie_id = 18148
        _BaseTMDbObject.__abstractmethods__ = frozenset()
        self.base = _BaseTMDbObject(self.movie_id) # pylint: disable=E0110

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
    def setUp(self):
        self.movie_id = 18148
        self.changed_movie = Movie(self.movie_id, preload=False)
        self.not_changed_movie = Movie(self.movie_id, preload=False)
        self.preloaded_movie = Movie(self.movie_id, preload=True)

    def test_raise_error_when_init_without_id(self):
        with self.assertRaises(KeyError):
            _ = Movie()

    def test_preloaded(self):
        movie = Movie(18148)
        movie.get_all()
        self.assertDictEqual(self.preloaded_movie.__dict__, movie.__dict__)

    def test_get_details(self):
        details = self.changed_movie.get_details()
        self.assertIsInstance(details, dict)
        for key in details.keys() - {"id"}:
            self.assertIn(key, self.changed_movie.__dict__)
            self.assertEqual(details[key], getattr(self.changed_movie, key))
            self.assertNotIn(key, self.not_changed_movie.__dict__)

    def test_get_alternative_titles(self):
        alternative_titles = self.changed_movie.get_alternative_titles()
        self.assertIsInstance(alternative_titles, dict)
        for key in alternative_titles.keys() - {"id"}:
            self.assertIn(key, self.changed_movie.__dict__)
            self.assertEqual(alternative_titles[key], getattr(self.changed_movie, key))
            self.assertNotIn(key, self.not_changed_movie.__dict__)
    
    def test_get_changes(self):
        changes = self.changed_movie.get_alternative_titles()
        self.assertIsInstance(changes, dict)
        for key in changes.keys() - {"id"}:
            self.assertIn(key, self.changed_movie.__dict__)
            self.assertEqual(changes[key], getattr(self.changed_movie, key))
            self.assertNotIn(key, self.not_changed_movie.__dict__)
    
    def test_get_credits(self):
        credits = self.changed_movie.get_alternative_titles()
        self.assertIsInstance(credits, dict)
        for key in credits.keys() - {"id"}:
            self.assertIn(key, self.changed_movie.__dict__)
            self.assertEqual(credits[key], getattr(self.changed_movie, key))
            self.assertNotIn(key, self.not_changed_movie.__dict__)

    def test_get_external_ids(self):
        external_ids = self.changed_movie.get_alternative_titles()
        self.assertIsInstance(external_ids, dict)
        for key in external_ids.keys() - {"id"}:
            self.assertIn(key, self.changed_movie.__dict__)
            self.assertEqual(external_ids[key], getattr(self.changed_movie, key))
            self.assertNotIn(key, self.not_changed_movie.__dict__)

    def test_get_images(self):
        images = self.changed_movie.get_alternative_titles()
        self.assertIsInstance(images, dict)
        for key in images.keys() - {"id"}:
            self.assertIn(key, self.changed_movie.__dict__)
            self.assertEqual(images[key], getattr(self.changed_movie, key))
            self.assertNotIn(key, self.not_changed_movie.__dict__)

    def test_get_keywords(self):
        keywords = self.changed_movie.get_alternative_titles()
        self.assertIsInstance(keywords, dict)
        for key in keywords.keys() - {"id"}:
            self.assertIn(key, self.changed_movie.__dict__)
            self.assertEqual(keywords[key], getattr(self.changed_movie, key))
            self.assertNotIn(key, self.not_changed_movie.__dict__)
    
    def test_get_release_dates(self):
        release_dates = self.changed_movie.get_alternative_titles()
        self.assertIsInstance(release_dates, dict)
        for key in release_dates.keys() - {"id"}:
            self.assertIn(key, self.changed_movie.__dict__)
            self.assertEqual(release_dates[key], getattr(self.changed_movie, key))
            self.assertNotIn(key, self.not_changed_movie.__dict__)

    def test_get_videos(self):
        videos = self.changed_movie.get_alternative_titles()
        self.assertIsInstance(videos, dict)
        for key in videos.keys() - {"id"}:
            self.assertIn(key, self.changed_movie.__dict__)
            self.assertEqual(videos[key], getattr(self.changed_movie, key))
            self.assertNotIn(key, self.not_changed_movie.__dict__)

    def test_get_translations(self):
        translations = self.changed_movie.get_alternative_titles()
        self.assertIsInstance(translations, dict)
        for key in translations.keys() - {"id"}:
            self.assertIn(key, self.changed_movie.__dict__)
            self.assertEqual(translations[key], getattr(self.changed_movie, key))
            self.assertNotIn(key, self.not_changed_movie.__dict__)

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
    pass


class PersonTestCase(unittest.TestCase):
    pass


class CompanyTestCase(unittest.TestCase):
    pass


if __name__ == "__main__":
    unittest.main()
