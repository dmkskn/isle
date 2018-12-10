import unittest

from themoviedb.objects.others import Credit, Image, Video, Vote
from themoviedb.objects.person import Person
from themoviedb.objects.show import Episode


class EpisodeTestCase(unittest.TestCase):
    def setUp(self):
        self.show_id = 66732
        self.s = 1  # season
        self.n = 1  # episode
        self.episode = Episode(self.n, show_id=self.show_id, season_number=self.s)

    def test_repr(self):
        self.assertEqual(self.episode.__repr__(), f"Episode({self.episode.tmdb_id})")

    def test_raise_error_when_init_without_show_id_with_season_number(self):
        with self.assertRaises(TypeError):
            _ = Episode()  # pylint: disable=E1120,E1125
        with self.assertRaises(TypeError):
            _ = Episode(self.n)  # pylint: disable=E1125
        with self.assertRaises(TypeError):
            _ = Episode(self.n, self.show_id)  # pylint: disable=E1121,E1125
        with self.assertRaises(TypeError):
            _ = Episode(self.n, show_id=self.show_id)  # pylint: disable=E1125

    def test_tmdb_id_attr(self):
        self.assertIsInstance(self.episode.tmdb_id, int)
        self.assertNotEqual(self.episode.tmdb_id, self.episode.show_id)

    def test_tvdb_id_attr(self):
        self.assertIsInstance(self.episode.tvdb_id, int)

    def test_imdb_id_attr(self):
        self.assertIsInstance(self.episode.imdb_id, str)

    def test_number_attr(self):
        self.assertIsInstance(self.episode.number, int)
        self.assertEqual(self.episode.number, self.episode.n)

    def test_season_number_attr(self):
        self.assertIsInstance(self.episode.season_number, int)
        self.assertEqual(self.episode.season_number, self.episode.sn)

    def test_title_attr(self):
        self.assertIsInstance(self.episode.title, dict)
        self.assertIn("default", self.episode.title)
        self.assertIn("US", self.episode.title)

    def test_overview_attr(self):
        self.assertIsInstance(self.episode.overview, dict)
        self.assertIn("default", self.episode.overview)
        self.assertIn("US", self.episode.overview)

    def test_air_date_attr(self):
        self.assertIsInstance(self.episode.air_date, str)
        self.assertEqual(len(self.episode.air_date.split("-")), 3)

    def test_stills_attr(self):
        self.assertIsInstance(self.episode.stills, list)
        self.assertIsInstance(self.episode.stills[0], Image)

    def test_videos_attr(self):
        self.assertIsInstance(self.episode.videos, list)
        if self.episode.videos:
            self.assertIsInstance(self.episode.videos[0], Video)

    def test_cast_attr(self):
        self.assertIsInstance(self.episode.cast, list)
        self.assertIsInstance(self.episode.cast[0], tuple)
        self.assertIsInstance(self.episode.cast[0][0], Person)
        self.assertIsInstance(self.episode.cast[0][1], Credit)

    def test_crew_attr(self):
        self.assertIsInstance(self.episode.crew, list)
        self.assertIsInstance(self.episode.cast[0], tuple)
        self.assertIsInstance(self.episode.cast[0][0], Person)
        self.assertIsInstance(self.episode.cast[0][1], Credit)

    def test_guest_stars_attr(self):
        self.assertIsInstance(self.episode.guest_stars, list)
        self.assertIsInstance(self.episode.guest_stars[0], tuple)
        self.assertIsInstance(self.episode.guest_stars[0][0], Person)
        self.assertIsInstance(self.episode.guest_stars[0][1], Credit)

    def test_vote_attr(self):
        self.assertIsInstance(self.episode.vote, Vote)

    def test_preloaded(self):
        first_dict = {"episode_number": self.n, "season_number": self.s}
        self.assertDictEqual(self.episode.data, first_dict)
        self.episode.get_all()
        self.assertNotEqual(self.episode.data, first_dict)

    def test_get_all(self):
        data = self.episode.get_all()
        self.assertDictEqual(data, self.episode.data)

    def test_get_details(self):
        details = self.episode.get_details()
        self.assertDictEqual(details, self.episode.data)

    def test_get_changes(self):
        changes = self.episode.get_changes()
        self.assertDictEqual(changes, self.episode.data["changes"])

    def test_get_external_ids(self):
        external_ids = self.episode.get_external_ids()
        self.assertDictEqual(external_ids, self.episode.data["external_ids"])

    def test_get_credits(self):
        credits = self.episode.get_credits()
        self.assertDictEqual(credits, self.episode.data["credits"])

    def test_get_images(self):
        images = self.episode.get_images()
        self.assertDictEqual(images, self.episode.data["images"])

    def test_get_videos(self):
        videos = self.episode.get_videos()
        self.assertDictEqual(videos, self.episode.data["videos"])


if __name__ == "__main__":
    unittest.main()
