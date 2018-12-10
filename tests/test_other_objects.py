import unittest
import inspect
from themoviedb.objects.movie import Movie
from themoviedb.objects.show import Show
from themoviedb.objects.person import Person
from themoviedb.objects.others import Credit, Genre, Image, Keyword, Vote


class KeywordTestCase(unittest.TestCase):
    def setUp(self):
        self.id_ = 3417
        self.name = "wormhole"
        self.keyword_without_name = Keyword(self.id_)
        self.keyword_with_name = Keyword(self.id_, name=self.name)

    def test_repr(self):
        self.assertEqual(self.keyword_with_name.__repr__(), f"Keyword({self.id_})")

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
        self.genre = Genre(tmdb_id=self.id_, name=self.name)

    def test_genre_id(self):
        self.assertEqual(self.genre.tmdb_id, self.id_)
        self.assertEqual(self.genre.tmdb_id, self.genre[0])

    def test_genre_name(self):
        self.assertEqual(self.genre.name, self.name)
        self.assertEqual(self.genre.name, self.genre[1])

    def test_genre_to_str(self):
        self.assertEqual(str(self.genre), self.name)


class ImageTestCase(unittest.TestCase):
    def setUp(self):
        self.data = {
            "aspect_ratio": 1.777_777_777_777_78,
            "file_path": "/fCayJrkfRaCRCTh8GqN30f8oyQF.jpg",
            "height": 720,
            "iso_639_1": None,
            "vote_average": 0,
            "vote_count": 0,
            "width": 1280,
        }
        self.image = Image(self.data, type_="backdrop")

    def test_init_without_type(self):
        with self.assertRaises(TypeError):
            _ = Image(self.data)  # pylint: disable=E1125

    def test_get_urls(self):
        self.assertEqual(self.image._configs_data, {})
        urls = self.image.url
        self.assertIsInstance(urls, dict)
        self.assertNotEqual(self.image._configs_data, {})

    def test_get_sizes(self):
        self.assertEqual(self.image._configs_data, {})
        sizes = self.image.sizes
        self.assertIsInstance(sizes, list)
        self.assertEqual(sizes, self.image._configs_data["backdrop_sizes"])


class CreditTestCase(unittest.TestCase):
    def setUp(self):
        self.movie_id = 18148
        self.show_id = 1399
        self.person_id = 287
        self.movie_credit_id = "52fe47639251416c750978a9"
        self.show_credit_id = "5256c8af19c2956ff60479f6"
        self.movie_crew_credit = Credit(self.movie_credit_id)
        self.show_cast_credit = Credit(self.show_credit_id)

    def test_init_without_id(self):
        with self.assertRaises(TypeError):
            _ = Credit()  # pylint: disable=E1120

    def test_credit_created_from_movie_object(self):
        movie = Movie(self.movie_id)
        movie.get_all()
        person, credit = movie.crew[0]
        person.get_all()
        self.assertIsInstance(credit, Credit)
        self.assertEqual(credit._media_data, movie.data)

    def test_credit_created_from_person_object(self):
        person = Person(self.person_id)
        person.get_all()
        _, credit = person.movie_cast[0]
        self.assertIsInstance(credit, Credit)
        self.assertEqual(credit._person_data, person.data)

    def test_get_details(self):
        data = self.movie_crew_credit.get_details()
        self.assertIsInstance(data, dict)
        self.assertIn("media", data)
        self.assertIn("person", data)
        self.assertIn("job", data)
        self.assertIn("department", data)

    def test_type_attr(self):
        self.assertEqual(self.movie_crew_credit.type, "crew")
        self.assertEqual(self.show_cast_credit.type, "cast")

    def test_media_type_attr(self):
        self.assertEqual(self.movie_crew_credit.media_type, "movie")
        self.assertEqual(self.show_cast_credit.media_type, "tv")

    def test_department_attr(self):
        self.assertIsInstance(self.movie_crew_credit.department, str)

    def test_job_attr(self):
        self.assertIsInstance(self.movie_crew_credit.job, str)

    def test_character_attr(self):
        self.assertIsNone(self.movie_crew_credit.character)
        self.assertIsInstance(self.show_cast_credit.character, str)

    def test_person_attr(self):
        self.assertIsInstance(self.movie_crew_credit.person, Person)

    def test_person_known_for_attr(self):
        self.assertIsInstance(self.movie_crew_credit.person_known_for, list)

    def test_media_attr(self):
        self.assertIsInstance(self.movie_crew_credit.media, Movie)
        self.assertIsInstance(self.show_cast_credit.media, Show)


if __name__ == "__main__":
    unittest.main()
