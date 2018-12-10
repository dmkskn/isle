import inspect
import re
import unittest

from themoviedb.objects.movie import Movie
from themoviedb.objects.person import Person
from themoviedb.objects.show import Show
from themoviedb.objects.others import (
    Country,
    Credit,
    Genre,
    Image,
    Keyword,
    Language,
    Video,
    Vote,
)


class PersonTestCase(unittest.TestCase):
    def setUp(self):
        self.person_id = 287
        self.person = Person(self.person_id)

    def test_repr(self):
        self.assertEqual(self.person.__repr__(), f"Person({self.person_id})")

    def test_raise_error_when_init_without_id(self):
        with self.assertRaises(TypeError):
            _ = Person()  # pylint: disable=E1120

    def test_name_attr(self):
        self.assertIsInstance(self.person.name, str)

    def test_also_known_as_attr(self):
        self.assertIsInstance(self.person.also_known_as, list)
        self.assertIsInstance(self.person.also_known_as[0], str)

    def test_birthday_attr(self):
        self.assertIsInstance(self.person.birthday, str)
        self.assertTrue(re.match(r"\d{4}-\d{2}-\d{2}", self.person.birthday))

    def test_known_for_department_attr(self):
        self.assertIsInstance(self.person.known_for_department, str)

    def test_deathday_attr(self):
        self.assertIsInstance(self.person.deathday, (str, type(None)))

    def test_gender_attr(self):
        self.assertIsInstance(self.person.gender, int)

    def test_biography_attr(self):
        self.assertIsInstance(self.person.biography, dict)
        self.assertIn("default", self.person.biography)
        self.assertIn("US", self.person.biography)

    def test_homepage_attr(self):
        self.assertIsInstance(self.person.homepage, (str, type(None)))

    def test_popularity_attr(self):
        self.assertIsInstance(self.person.popularity, float)

    def test_place_of_birth_attr(self):
        self.assertIsInstance(self.person.place_of_birth, str)

    def test_is_adult_attr(self):
        self.assertIsInstance(self.person.is_adult, bool)

    def test_movie_cast_attr(self):
        self.assertIsInstance(self.person.movie_cast, list)
        self.assertIsInstance(self.person.movie_cast[0], tuple)
        self.assertIsInstance(self.person.movie_cast[0][0], Movie)
        self.assertIsInstance(self.person.movie_cast[0][1], Credit)

    def test_movie_crew_attr(self):
        self.assertIsInstance(self.person.movie_crew, list)
        self.assertIsInstance(self.person.movie_crew[0], tuple)
        self.assertIsInstance(self.person.movie_crew[0][0], Movie)
        self.assertIsInstance(self.person.movie_crew[0][1], Credit)

    def test_show_cast_attr(self):
        self.assertIsInstance(self.person.show_cast, list)
        self.assertIsInstance(self.person.show_cast[0], tuple)
        self.assertIsInstance(self.person.show_cast[0][0], Show)
        self.assertIsInstance(self.person.show_cast[0][1], Credit)

    def test_show_crew_attr(self):
        self.assertIsInstance(self.person.show_crew, list)
        self.assertIsInstance(self.person.show_crew[0], tuple)
        self.assertIsInstance(self.person.show_crew[0][0], Show)
        self.assertIsInstance(self.person.show_crew[0][1], Credit)

    def test_cast_attr(self):
        self.assertIsInstance(self.person.cast, list)
        self.assertIsInstance(self.person.cast[0], tuple)
        self.assertIsInstance(self.person.cast[0][0], (Show, Movie))
        self.assertIsInstance(self.person.cast[0][1], Credit)

    def test_crew_attr(self):
        self.assertIsInstance(self.person.crew, list)
        self.assertIsInstance(self.person.crew[0], tuple)
        self.assertIsInstance(self.person.crew[0][0], (Show, Movie))
        self.assertIsInstance(self.person.crew[0][1], Credit)

    def test_external_ids_attrs(self):
        imdb_id = self.person.imdb_id
        freebase_mid = self.person.freebase_mid
        freebase_id = self.person.freebase_id
        tvrage_id = self.person.tvrage_id
        facebook_id = self.person.facebook_id
        instagram_id = self.person.instagram_id
        twitter_id = self.person.twitter_id
        self.assertEqual(imdb_id, self.person.data["external_ids"]["imdb_id"])
        self.assertEqual(freebase_mid, self.person.data["external_ids"]["freebase_mid"])
        self.assertEqual(freebase_id, self.person.data["external_ids"]["freebase_id"])
        self.assertEqual(tvrage_id, self.person.data["external_ids"]["tvrage_id"])
        self.assertEqual(facebook_id, self.person.data["external_ids"]["facebook_id"])
        self.assertEqual(instagram_id, self.person.data["external_ids"]["instagram_id"])
        self.assertEqual(twitter_id, self.person.data["external_ids"]["twitter_id"])

    def test_profiles_attr(self):
        self.assertIsInstance(self.person.profiles, list)
        self.assertIsInstance(self.person.profiles[0], Image)

    def test_preloaded(self):
        self.assertDictEqual(self.person.data, {"id": self.person_id})
        self.person.get_all()
        self.assertNotEqual(self.person.data, {"id": self.person_id})

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


if __name__ == "__main__":
    unittest.main()
