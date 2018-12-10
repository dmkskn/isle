import inspect
import unittest

from themoviedb.objects.company import Company
from themoviedb.objects.movie import Movie
from themoviedb.objects.person import Person
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


class MovieTestCase(unittest.TestCase):
    def setUp(self):
        self.movie_id = 18148  # there are tests that depend on the movie id
        self.movie = Movie(self.movie_id)

    def test_repr(self):
        self.assertEqual(self.movie.__repr__(), f"Movie({self.movie_id})")

    def test_raise_error_when_init_without_id(self):
        with self.assertRaises(TypeError):
            _ = Movie()  # pylint: disable=E1120

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

    def test_releases_attr(self):
        releases = self.movie.releases
        self.assertIsInstance(releases, dict)
        release_dates_data = self.movie.data["release_dates"]["results"]
        for key in (x["iso_3166_1"] for x in release_dates_data):
            self.assertIn(key, releases)
        us_releases = releases["US"]
        release = us_releases[0]
        self.assertIsInstance(us_releases, list)
        self.assertIsInstance(release, dict)
        self.assertIn("certification", release)
        self.assertIn("date", release)
        self.assertIn("note", release)
        self.assertIn("type", release)
        self.assertNotIn("release_date", release)
        self.assertNotIn("iso_639_1", release)

    def test_is_adult_attr(self):
        self.assertIsInstance(self.movie.is_adult, bool)

    def test_backdrops_attr(self):
        self.assertIsInstance(self.movie.backdrops, list)
        self.assertIsInstance(self.movie.backdrops[0], Image)

    def test_posters_attr(self):
        self.assertIsInstance(self.movie.posters, list)
        self.assertIsInstance(self.movie.posters[0], Image)

    def test_languages_attr(self):
        self.assertIsInstance(self.movie.languages, list)
        self.assertIsInstance(self.movie.languages[0], Language)

    def test_popularity_attr(self):
        self.assertIsInstance(self.movie.popularity, float)

    def test_homepage_attr(self):
        self.assertIsInstance(self.movie.homepage, dict)

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
        self.assertIsInstance(self.movie.cast[0], tuple)
        self.assertIsInstance(self.movie.cast[0][0], Person)
        self.assertIsInstance(self.movie.cast[0][1], Credit)

    def test_crew_attr(self):
        self.assertIsInstance(self.movie.crew, list)
        self.assertIsInstance(self.movie.crew[0], tuple)
        self.assertIsInstance(self.movie.crew[0][0], Person)
        self.assertIsInstance(self.movie.crew[0][1], Credit)

    def test_videos_attr(self):
        self.assertIsInstance(self.movie.videos, list)
        if self.movie.videos:
            self.assertIsInstance(self.movie.videos[0], Video)

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
        self.assertIsInstance(self.movie.vote, Vote)

    def test_countries_attr(self):
        self.assertIsInstance(self.movie.countries, list)
        self.assertIsInstance(self.movie.countries[0], Country)

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


if __name__ == "__main__":
    unittest.main()
