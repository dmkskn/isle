import unittest

from themoviedb.objects.others import Credit, Image, Video
from themoviedb.objects.person import Person
from themoviedb.objects.show import Episode, Season


class SeasonTestCase(unittest.TestCase):
    def setUp(self):
        self.show_id = 66732
        self.n = 1
        self.season = Season(self.n, show_id=self.show_id)

    def test_repr(self):
        self.assertEqual(self.season.__repr__(), f"Season({self.season.tmdb_id})")

    def test_raise_error_when_init_without_show_id_with_season_number(self):
        with self.assertRaises(TypeError):
            _ = Season()  # pylint: disable=E1120,E1125
        with self.assertRaises(TypeError):
            _ = Season(1)  # pylint: disable=E1125
        with self.assertRaises(TypeError):
            _ = Season(  # pylint: disable=E1125
                {"show_id": self.show_id, "season_number": 1}
            )
        with self.assertRaises(TypeError):
            _ = Season(self.show_id)  # pylint: disable=E1125

    def test_tmdb_id_attr(self):
        self.assertIsInstance(self.season.tmdb_id, int)
        self.assertNotEqual(self.season.tmdb_id, self.season.show_id)

    def test_tvdb_id_attr(self):
        self.assertIsInstance(self.season.tvdb_id, int)

    def test_number_attr(self):
        self.assertIsInstance(self.season.number, int)
        self.assertEqual(self.season.number, self.season.n)

    def test_title_attr(self):
        self.assertIsInstance(self.season.title, str)

    def test_overview_attr(self):
        self.assertIsInstance(self.season.overview, str)

    def test_air_date_attr(self):
        self.assertIsInstance(self.season.air_date, str)
        self.assertEqual(len(self.season.air_date.split("-")), 3)

    def test_episodes_attr(self):
        self.assertIsInstance(self.season.episodes, list)
        self.assertIsInstance(self.season.episodes[0], Episode)

    def test_posters_attr(self):
        self.assertIsInstance(self.season.posters, list)
        self.assertIsInstance(self.season.posters[0], Image)

    def test_videos_attr(self):
        self.assertIsInstance(self.season.videos, list)
        if self.season.videos:
            self.assertIsInstance(self.season.videos[0], Video)

    def test_cast_attr(self):
        self.assertIsInstance(self.season.cast, list)
        self.assertIsInstance(self.season.cast[0], tuple)
        self.assertIsInstance(self.season.cast[0][0], Person)
        self.assertIsInstance(self.season.cast[0][1], Credit)

    def test_crew_attr(self):
        self.assertIsInstance(self.season.crew, list)
        self.assertIsInstance(self.season.crew[0], tuple)
        self.assertIsInstance(self.season.crew[0][0], Person)
        self.assertIsInstance(self.season.crew[0][1], Credit)

    def test_preloaded(self):
        self.assertDictEqual(self.season.data, {"season_number": self.n})
        self.season.get_all()
        self.assertNotEqual(self.season.data, {"season_number": self.n})

    def test_get_all(self):
        data = self.season.get_all()
        self.assertDictEqual(data, self.season.data)

    def test_get_details(self):
        details = self.season.get_details()
        self.assertDictEqual(details, self.season.data)

    def test_get_changes(self):
        changes = self.season.get_changes()
        self.assertDictEqual(changes, self.season.data["changes"])

    def test_get_external_ids(self):
        external_ids = self.season.get_external_ids()
        self.assertDictEqual(external_ids, self.season.data["external_ids"])

    def test_get_credits(self):
        credits = self.season.get_credits()
        self.assertDictEqual(credits, self.season.data["credits"])

    def test_get_images(self):
        images = self.season.get_images()
        self.assertDictEqual(images, self.season.data["images"])

    def test_get_videos(self):
        videos = self.season.get_videos()
        self.assertDictEqual(videos, self.season.data["videos"])


if __name__ == "__main__":
    unittest.main()
