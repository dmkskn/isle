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
        self.movie = Movie(self.movie_id)

    def test_raise_error_when_init_without_id(self):
        with self.assertRaises(TypeError):
            _ = Movie()  # pylint: disable=E1120
        with self.assertRaises(TypeError):
            _ = Movie("not int")
        with self.assertRaises(TypeError):
            _ = Movie({"id": self.movie_id})

    def test_title_attr(self):
        self.assertIsInstance(self.movie.title, dict)
        self.assertIn("original", self.movie.title)
        self.assertIn("default", self.movie.title)
        self.assertIn("US", self.movie.title)

    def test_overview_attr(self):
        self.assertIsInstance(self.movie.overview, dict)
        self.assertIn("default", self.movie.overview)
        self.assertIn("US", self.movie.overview)

    def test_tagline_attr(self):
        self.assertIsInstance(self.movie.tagline, str)

    def test_year_attr(self):
        self.assertIsInstance(self.movie.year, int)
        self.assertEqual(len(str(self.movie.year)), 4)

    def test_external_ids_attrs(self):
        imdb_id = self.movie.imdb_id
        facebook_id = self.movie.facebook_id
        instagram_id = self.movie.instagram_id
        twitter_id = self.movie.twitter_id
        self.assertEqual(imdb_id, self.movie.data["external_ids"]["imdb_id"])
        self.assertEqual(facebook_id, self.movie.data["external_ids"]["facebook_id"])
        self.assertEqual(instagram_id, self.movie.data["external_ids"]["instagram_id"])
        self.assertEqual(twitter_id, self.movie.data["external_ids"]["twitter_id"])

    def test_release_dates_attr(self):
        dates = self.movie.release_dates
        self.assertIsInstance(dates, dict)
        release_dates = self.movie.data["release_dates"]["results"]
        for key in (x["iso_3166_1"] for x in release_dates):
            self.assertIn(key, dates)
        self.assertIsInstance(dates["US"], list)

    def test_is_adult_attr(self):
        self.assertIsInstance(self.movie.is_adult, bool)

    def test_backdrops_attr(self):
        self.assertIsInstance(self.movie.backdrops, list)
        self.assertIsInstance(self.movie.backdrops[0], dict)

    def test_posters_attr(self):
        self.assertIsInstance(self.movie.posters, list)
        self.assertIsInstance(self.movie.posters[0], dict)

    def test_languages_attr(self):
        self.assertIsInstance(self.movie.languages, list)

    def test_popularity_attr(self):
        self.assertIsInstance(self.movie.popularity, float)

    def test_homepage_attr(self):
        self.assertIsInstance(self.movie.homepage, dict)
        self.assertIn("default", self.movie.homepage)
        self.assertIn("US", self.movie.homepage)

    def test_revenue_attr(self):
        self.assertIsInstance(self.movie.revenue, int)

    def test_budget_attr(self):
        self.assertIsInstance(self.movie.budget, int)

    def test_runtime_attr(self):
        self.assertIsInstance(self.movie.runtime, int)

    def test_status_attr(self):
        self.assertIsInstance(self.movie.status, str)

    def test_cast_attr(self):
        self.assertIsInstance(self.movie.cast, list)
        self.assertIsInstance(self.movie.cast[0], dict)
        self.assertIsInstance(self.movie.cast[0]["person"], Person)

    def test_crew_attr(self):
        self.assertIsInstance(self.movie.crew, list)
        self.assertIsInstance(self.movie.crew[0], dict)
        self.assertIsInstance(self.movie.crew[0]["person"], Person)

    def test_videos_attr(self):
        self.assertIsInstance(self.movie.videos, list)
        self.assertIsInstance(self.movie.videos[0], dict)

    def test_keywords_attr(self):
        seen_keywords = []
        for keyword in self.movie.keywords:
            self.assertIsInstance(keyword, Keyword)
            self.assertNotIn(keyword, seen_keywords)
            seen_keywords.append(keyword)

    def test_genres_attr(self):
        seen_genres = []
        for genre in self.movie.genres:
            self.assertIsInstance(genre, Genre)
            self.assertNotIn(genre, seen_genres)
            seen_genres.append(genre)

    def test_companies_attr(self):
        seen_companies = []
        for company in self.movie.companies:
            self.assertIsInstance(company, Company)
            self.assertNotIn(company, seen_companies)
            seen_companies.append(company)

    def test_vote_attr(self):
        self.assertIsInstance(self.movie.vote, tuple)

    def test_countries_attr(self):
        self.assertIsInstance(self.movie.countries, list)

    def test_raise_error_when_init_without_id(self):
        with self.assertRaises(TypeError):
            _ = Movie()  # pylint: disable=E1120

    def test_preloaded(self):
        self.assertDictEqual(self.movie.data, {"id": self.movie_id})
        self.movie.get_all()
        self.assertNotEqual(self.movie.data, {"id": self.movie_id})

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
        self.show = Show(self.show_id)

    def test_raise_error_when_init_without_id(self):
        with self.assertRaises(TypeError):
            _ = Show()  # pylint: disable=E1120
        with self.assertRaises(TypeError):
            _ = Show("not int")
        with self.assertRaises(TypeError):
            _ = Show({"id": self.show_id})

    def test_preloaded(self):
        self.assertDictEqual(self.show.data, {"id": self.show_id})
        self.show.get_all()
        self.assertNotEqual(self.show.data, {"id": self.show_id})

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
        self.person = Person(self.person_id)

    def test_raise_error_when_init_without_id(self):
        with self.assertRaises(TypeError):
            _ = Person()  # pylint: disable=E1120
        with self.assertRaises(TypeError):
            _ = Person("not int")
        with self.assertRaises(TypeError):
            _ = Person({"id": self.person_id})

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


class CompanyTestCase(unittest.TestCase):
    def setUp(self):
        self.company_id = 1
        self.company = Company(self.company_id)

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
        self.keyword_without_name = Keyword(self.id_)
        self.keyword_with_name = Keyword(self.id_, name=self.name)

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
        self.genre = Genre(self.id_, name=self.name)

    def test_init_genre(self):
        expected_data = {"id": self.id_, "name": self.name}
        self.assertDictEqual(self.genre.data, expected_data)

    def test_genre_to_str(self):
        self.assertEqual(str(self.genre), self.name)


if __name__ == "__main__":
    unittest.main()
