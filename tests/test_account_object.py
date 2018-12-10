import os
import unittest
import inspect
from themoviedb.objects.account import Account, TMDbList
from themoviedb.objects.movie import Movie
from themoviedb.objects.show import Show, Episode
from themoviedb.objects.others import Language


class AccountTestCase(unittest.TestCase):
    USERNAME = os.getenv("TMDB_USERNAME")
    PASSWORD = os.getenv("TMDB_PASSWORD")

    def setUp(self):
        self.account = Account()

    @classmethod
    def setUpClass(cls):
        cls.logged_account = Account()
        cls.logged_account.login(cls.USERNAME, cls.PASSWORD)

    def test_login(self):
        r = self.account.login(self.USERNAME, self.PASSWORD)
        self.assertTrue(r["success"])

    def test_logout(self):
        self.account.login(self.USERNAME, self.PASSWORD)
        r = self.account.logout()
        self.assertTrue(r["success"])

    def test_saves_session_id(self):
        with self.assertRaises(Account.SessionError):
            self.account._session_id
        self.account.login(self.USERNAME, self.PASSWORD)
        self.assertIsInstance(self.account._session, Account._Session)

    def test_saves_token_id(self):
        with self.assertRaises(Account.TokenError):
            self.account._token_id
        self.account._create_token()
        self.account._validate_token(self.USERNAME, self.PASSWORD)
        self.assertIsInstance(self.account._token, Account._Token)

    def test_get_details(self):
        details = self.logged_account.get_details()
        self.assertIsInstance(details, dict)
        self.assertIn("avatar", details)
        self.assertIn("name", details)
        self.assertIn("username", details)

    def test_properties(self):
        self.account.login(self.USERNAME, self.PASSWORD)
        self.assertEqual(self.account.data, {})
        n = self.account.n_requests
        self.assertIsInstance(self.account.username, str)
        self.assertIsInstance(self.account.fallback_language, str)
        self.assertIsInstance(self.account.default_language, str)
        self.assertNotEqual(self.account.data, {})
        self.assertEqual(self.account.n_requests, n + 1)

    def test_iter_lists(self):
        lists = self.logged_account.iter_lists()
        self.assertTrue(inspect.isgenerator(lists))
        for l in lists:
            self.assertIsInstance(l, TMDbList)

    def test_iter_favorite_movies(self):
        favorite_movies = self.logged_account.iter_favorite_movies()
        self.assertTrue(inspect.isgenerator(favorite_movies))
        for movie in favorite_movies:
            self.assertIsInstance(movie, Movie)

    def test_iter_favorite_shows(self):
        favorite_shows = self.logged_account.iter_favorite_shows()
        self.assertTrue(inspect.isgenerator(favorite_shows))
        for show in favorite_shows:
            self.assertIsInstance(show, Show)

    def test_iter_rated_movies(self):
        rated_movies = self.logged_account.iter_rated_movies()
        self.assertTrue(inspect.isgenerator(rated_movies))
        for movie in rated_movies:
            self.assertIsInstance(movie, Movie)

    def test_iter_rated_shows(self):
        rated_shows = self.logged_account.iter_rated_shows()
        self.assertTrue(inspect.isgenerator(rated_shows))
        for show in rated_shows:
            self.assertIsInstance(show, Show)

    def test_iter_rated_episodes(self):
        rated_episodes = self.logged_account.iter_rated_episodes()
        self.assertTrue(inspect.isgenerator(rated_episodes))
        for episode in rated_episodes:
            self.assertIsInstance(episode, Episode)

    def test_iter_movie_watchlist(self):
        movie_watchlist = self.logged_account.iter_movie_watchlist()
        self.assertTrue(inspect.isgenerator(movie_watchlist))
        for movie in movie_watchlist:
            self.assertIsInstance(movie, Movie)

    def test_iter_show_watchlist(self):
        show_watchlist = self.logged_account.iter_show_watchlist()
        self.assertTrue(inspect.isgenerator(show_watchlist))
        for movie in show_watchlist:
            self.assertIsInstance(movie, Show)

    def test_mark_as_favorite(self):
        r = self.logged_account.remove_from_favorites(Movie(18148))
        r = self.logged_account.mark_as_favorite(Movie(18148))
        self.assertEqual(r["status_code"], 1)

    def test_remove_from_favorite(self):
        r = self.logged_account.remove_from_favorites(Movie(18148))
        self.assertEqual(r["status_code"], 13)

    def test_add_to_watchlist(self):
        r = self.logged_account.remove_from_watchlist(Movie(18148))
        r = self.logged_account.add_to_watchlist(Movie(18148))
        self.assertEqual(r["status_code"], 1)

    def test_remove_from_watchlist(self):
        r = self.logged_account.remove_from_watchlist(Movie(18148))
        self.assertEqual(r["status_code"], 13)

    def test_rate(self):
        r = self.logged_account.rate(Movie(18148), 8.5)
        self.assertEqual(r["status_code"], 1)

    def test_delete_rating(self):
        r = self.logged_account.delete_rating(Movie(18148))
        self.assertEqual(r["status_code"], 13)

    # def test_create_list(self):
    #     l = self.logged_account.create_list("name", "desc")
    #     self.assertIsInstance(l, TMDbList)
    #     self.assertEqual(l.name, "name")
    #     self.assertEqual(l.description, "desc")
    #     self.logged_account.delete_list(l)

    # def test_delete_list(self):
    #     l = self.logged_account.create_list("name_del", "desc_del")
    #     r = self.logged_account.delete_list(l)
    #     self.assertEqual(r["status_code"], 13)

    # def test_add_movie_to_list(self):
    #     l = self.logged_account.create_list("name", "desc")
    #     r = self.logged_account.add_movie_to_list(l, Movie(18148))
    #     self.assertEqual(r["status_code"], 12)
    #     self.assertTrue(l._changed)
    #     self.assertTrue(l.has_movie(Movie(18148)))
    #     self.assertTrue(any([m.tmdb_id == 18148 for m in l.items]))
    #     self.logged_account.delete_list(l)

    # def test_remove_movie_from_list(self):
    #     l = self.logged_account.create_list("name", "desc")
    #     self.logged_account.add_movie_to_list(l, Movie(18148))
    #     r = self.logged_account.remove_movie_from_list(l, Movie(18148))
    #     self.assertEqual(r["status_code"], 13)
    #     self.assertTrue(l._changed)
    #     self.assertTrue(not l.has_movie(Movie(18148)))
    #     self.logged_account.delete_list(l)

    # def test_clear_list(self):
    #     l = self.logged_account.create_list("name", "desc")
    #     self.logged_account.add_movie_to_list(l, Movie(18148))
    #     self.logged_account.add_movie_to_list(l, Movie(238))
    #     r = self.logged_account.clear_list(l)
    #     self.assertEqual(r["status_code"], 12)
    #     self.assertTrue(l._changed)
    #     self.assertEqual(l.items, [])
    #     self.assertTrue(not l.has_movie(Movie(18148)))
    #     self.assertTrue(not l.has_movie(Movie(238)))


class ListTestCase(unittest.TestCase):
    LIST_ID = os.getenv("TMDB_LIST_ID")

    def setUp(self):
        self.list_ = TMDbList(self.LIST_ID)

    def test_name_attr(self):
        self.assertEqual(self.list_.name, self.list_.data["name"])

    def test_description_attr(self):
        self.assertEqual(self.list_.description, self.list_.data["description"])

    def test_creator_attr(self):
        self.assertEqual(self.list_.creator, self.list_.data["created_by"])

    def test_n_favorites_attr(self):
        self.assertEqual(self.list_.n_favorites, self.list_.data["favorite_count"])

    def test_items_attr(self):
        for item in self.list_.items:
            self.assertIsInstance(item, (Movie, Show))

    def test_language_attr(self):
        self.assertIsInstance(self.list_.language, Language)

    def test_get_details(self):
        details = self.list_.get_details()
        self.assertIsInstance(details, dict)
        self.assertIn("name", details)
        self.assertEqual(details, self.list_.data)

    def test_has_movie(self):
        for item in self.list_.items:
            if isinstance(item, Movie):
                self.assertTrue(self.list_.has_movie(item))
                break


if __name__ == "__main__":
    unittest.main()
