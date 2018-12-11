import inspect
import unittest

from themoviedb.objects.company import Company
from themoviedb.objects.show import Show, Season, Episode
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


class ShowTestCase(unittest.TestCase):
    def setUp(self):
        self.show_id = 1399
        self.show = Show(self.show_id)

    def test_repr(self):
        self.assertEqual(self.show.__repr__(), f"Show({self.show_id})")

    def test_title_attr(self):
        self.assertIsInstance(self.show.title, dict)
        self.assertIn("original", self.show.title)
        self.assertIn("default", self.show.title)
        self.assertIn("RU", self.show.title)

    def test_overview_attr(self):
        self.assertIsInstance(self.show.overview, dict)
        self.assertIn("default", self.show.overview)
        self.assertIn("US", self.show.overview)

    def test_creators_attr(self):
        self.assertIsInstance(self.show.creators, list)
        self.assertIsInstance(self.show.creators[0], Person)

    def test_runtimes_attr(self):
        self.assertIsInstance(self.show.runtimes, list)
        self.assertIsInstance(self.show.runtimes[0], int)

    def test_first_air_date_attr(self):
        self.assertIsInstance(self.show.first_air_date, str)

    def test_last_air_date_attr(self):
        self.assertIsInstance(self.show.last_air_date, str)

    def test_homepage_attr(self):
        self.assertIsInstance(self.show.homepage, dict)
        self.assertIn("default", self.show.homepage)

    def test_in_production_attr(self):
        self.assertIsInstance(self.show.in_production, bool)

    def test_languages_attr(self):
        self.assertIsInstance(self.show.languages, list)
        self.assertIsInstance(self.show.languages[0], Language)

    def test_last_episode_attr(self):
        self.assertIsInstance(self.show.last_episode, Episode)

    def test_next_episode_attr(self):
        self.assertIsInstance(self.show.next_episode, (Episode, type(None)))

    def test_n_episodes_attr(self):
        self.assertIsInstance(self.show.n_episodes, int)

    def test_n_seasons_attr(self):
        self.assertIsInstance(self.show.n_seasons, int)

    def test_countries_attr(self):
        self.assertIsInstance(self.show.countries, list)
        self.assertIsInstance(self.show.countries[0], Country)

    def test_popularity_attr(self):
        self.assertIsInstance(self.show.popularity, float)

    def test_companies_attr(self):
        self.assertIsInstance(self.show.companies, list)
        self.assertIsInstance(self.show.companies[0], Company)

    def test_seasons_attr(self):
        self.assertIsInstance(self.show.seasons, list)
        self.assertIsInstance(self.show.seasons[0], Season)

    def test_status_attr(self):
        self.assertIsInstance(self.show.status, str)

    def test_type_attr(self):
        self.assertIsInstance(self.show.type, str)

    def test_vote_attr(self):
        self.assertIsInstance(self.show.vote, Vote)
        self.assertIsInstance(self.show.vote[0], float)
        self.assertIsInstance(self.show.vote[1], int)

    def test_ratings_attr(self):
        self.assertIsInstance(self.show.ratings, dict)
        for iso, rating in self.show.ratings.items():
            self.assertIsInstance(iso, str)
            self.assertEqual(len(iso), 2)
            self.assertIsInstance(rating, str)

    def test_cast_attr(self):
        self.assertIsInstance(self.show.cast, list)
        self.assertIsInstance(self.show.cast[0], tuple)
        self.assertIsInstance(self.show.cast[0][0], Person)
        self.assertIsInstance(self.show.cast[0][1], Credit)

    def test_crew_attr(self):
        self.assertIsInstance(self.show.crew, list)
        self.assertIsInstance(self.show.crew[0], tuple)
        self.assertIsInstance(self.show.crew[0][0], Person)
        self.assertIsInstance(self.show.crew[0][1], Credit)

    def test_external_ids_attrs(self):
        imdb_id = self.show.imdb_id
        tvdb_id = self.show.tvdb_id
        facebook_id = self.show.facebook_id
        instagram_id = self.show.instagram_id
        twitter_id = self.show.twitter_id
        self.assertEqual(imdb_id, self.show.data["external_ids"]["imdb_id"])
        self.assertEqual(tvdb_id, self.show.data["external_ids"]["tvdb_id"])
        self.assertEqual(facebook_id, self.show.data["external_ids"]["facebook_id"])
        self.assertEqual(instagram_id, self.show.data["external_ids"]["instagram_id"])
        self.assertEqual(twitter_id, self.show.data["external_ids"]["twitter_id"])

    def test_backdrops_attr(self):
        self.assertIsInstance(self.show.backdrops, list)
        self.assertIsInstance(self.show.backdrops[0], Image)

    def test_posters_attr(self):
        self.assertIsInstance(self.show.posters, list)
        self.assertIsInstance(self.show.posters[0], Image)

    def test_keywords_attr(self):
        seen_keywords = []
        for keyword in self.show.keywords:
            self.assertIsInstance(keyword, Keyword)
            self.assertNotIn(keyword, seen_keywords)
            seen_keywords.append(keyword)

    def test_genres_attr(self):
        seen_genres = []
        for genre in self.show.genres:
            self.assertIsInstance(genre, Genre)
            self.assertNotIn(genre, seen_genres)
            seen_genres.append(genre)

    def test_videos_attr(self):
        self.assertIsInstance(self.show.videos, list)
        if self.show.videos:
            self.assertIsInstance(self.show.videos[0], Video)

    def test_raise_error_when_init_without_id(self):
        with self.assertRaises(TypeError):
            _ = Show()  # pylint: disable=E1120

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


if __name__ == "__main__":
    unittest.main()
