import re
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

    def test_name_attr(self):
        self.assertIsInstance(self.show.name, dict)
        self.assertIn("original", self.show.name)
        self.assertIn("default", self.show.name)
        self.assertIn("US", self.show.name)

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
        self.assertIn("US", self.show.homepage)

    def test_in_production_attr(self):
        self.assertIsInstance(self.show.in_production, bool)

    def test_languages_attr(self):
        self.assertIsInstance(self.show.languages, list)
        self.assertIsInstance(self.show.languages[0], str)
        self.assertEqual(len(self.show.languages[0]), 2)

    def test_last_episode_attr(self):
        self.assertIsInstance(self.show.last_episode, dict)

    def test_next_episode_attr(self):
        self.assertIsInstance(self.show.next_episode, (dict, type(None)))

    def test_n_episodes_attr(self):
        self.assertIsInstance(self.show.n_episodes, int)

    def test_n_seasons_attr(self):
        self.assertIsInstance(self.show.n_seasons, int)

    def test_countries_attr(self):
        self.assertIsInstance(self.show.countries, list)
        self.assertIsInstance(self.show.countries[0], str)
        self.assertEqual(len(self.show.countries[0]), 2)

    def test_popularity_attr(self):
        self.assertIsInstance(self.show.popularity, float)

    def test_companies_attr(self):
        self.assertIsInstance(self.show.companies, list)
        self.assertIsInstance(self.show.companies[0], Company)

    def test_seasons_attr(self):
        self.assertIsInstance(self.show.seasons, list)
        self.assertIsInstance(self.show.seasons[0], dict)

    def test_status_attr(self):
        self.assertIsInstance(self.show.status, str)

    def test_type_attr(self):
        self.assertIsInstance(self.show.type, str)

    def test_vote_attr(self):
        self.assertIsInstance(self.show.vote, tuple)
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
        self.assertIsInstance(self.show.cast[0], dict)
        self.assertIsInstance(self.show.cast[0]["person"], Person)

    def test_crew_attr(self):
        self.assertIsInstance(self.show.crew, list)
        self.assertIsInstance(self.show.crew[0], dict)
        self.assertIsInstance(self.show.crew[0]["person"], Person)

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
        self.assertIsInstance(self.show.backdrops[0], dict)

    def test_posters_attr(self):
        self.assertIsInstance(self.show.posters, list)
        self.assertIsInstance(self.show.posters[0], dict)

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
        self.assertIsInstance(self.show.videos[0], dict)
        self.assertIn("type", self.show.videos[0])
        self.assertIn("site", self.show.videos[0])
        self.assertIn("size", self.show.videos[0])
        self.assertIn("key", self.show.videos[0])

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
        self.assertIsInstance(self.person.movie_cast[0], dict)
        self.assertIn("character", self.person.movie_cast[0])
        self.assertIn("movie", self.person.movie_cast[0])
        self.assertIsInstance(self.person.movie_cast[0]["movie"], Movie)

    def test_movie_crew_attr(self):
        self.assertIsInstance(self.person.movie_crew, list)
        self.assertIsInstance(self.person.movie_crew[0], dict)
        self.assertIn("department", self.person.movie_crew[0])
        self.assertIn("job", self.person.movie_crew[0])
        self.assertIn("movie", self.person.movie_crew[0])
        self.assertIsInstance(self.person.movie_crew[0]["movie"], Movie)

    def test_show_cast_attr(self):
        self.assertIsInstance(self.person.show_cast, list)
        self.assertIsInstance(self.person.show_cast[0], dict)
        self.assertIn("character", self.person.show_cast[0])
        self.assertIn("show", self.person.show_cast[0])
        self.assertIsInstance(self.person.show_cast[0]["show"], Show)

    def test_show_crew_attr(self):
        self.assertIsInstance(self.person.show_crew, list)
        self.assertIsInstance(self.person.show_crew[0], dict)
        self.assertIn("department", self.person.show_crew[0])
        self.assertIn("job", self.person.show_crew[0])
        self.assertIn("show", self.person.show_crew[0])
        self.assertIsInstance(self.person.show_crew[0]["show"], Show)

    def test_cast_attr(self):
        self.assertIsInstance(self.person.cast, list)
        self.assertIsInstance(self.person.cast[0], dict)
        self.assertIn("character", self.person.cast[0])
        self.assertIn("media_type", self.person.cast[0])
        if self.person.cast[0]["media_type"] == "tv":
            self.assertIn("show", self.person.cast[0])
            self.assertIsInstance(self.person.cast[0]["show"], Show)
        else:
            self.assertIn("movie", self.person.cast[0])
            self.assertIsInstance(self.person.cast[0]["movie"], Movie)

    def test_crew_attr(self):
        self.assertIsInstance(self.person.crew, list)
        self.assertIsInstance(self.person.crew[0], dict)
        self.assertIn("department", self.person.crew[0])
        self.assertIn("job", self.person.crew[0])
        self.assertIn("media_type", self.person.crew[0])
        if self.person.crew[0]["media_type"] == "tv":
            self.assertIn("show", self.person.crew[0])
            self.assertIsInstance(self.person.crew[0]["show"], Show)
        else:
            self.assertIn("movie", self.person.crew[0])
            self.assertIsInstance(self.person.crew[0]["movie"], Movie)

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
        self.assertIsInstance(self.person.profiles[0], dict)

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
