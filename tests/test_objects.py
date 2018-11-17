import re
import unittest
import inspect
from themoviedb._objects import (
    TMDb,
    Movie,
    Show,
    Person,
    Company,
    Keyword,
    Genre,
    Season,
    Episode,
    Image,
    Language,
    Vote,
    Country,
    Video,
    Credit,
)


class TMDbTestCase(unittest.TestCase):
    def setUp(self):
        self.movie_id = 18148
        TMDb.__abstractmethods__ = frozenset()
        self.base = TMDb(self.movie_id)  # pylint: disable=E0110

    def test_request(self):
        url = f"https://api.themoviedb.org/3/movie/{self.movie_id}"
        params = {}
        self.assertEqual(self.base.n_requests, 0)
        res = self.base._request(url, **params)
        self.assertEqual(res["original_title"], "東京物語")
        self.assertEqual(self.base.n_requests, 1)

    def test_iter_request(self):
        url = f"https://api.themoviedb.org/3/movie/{self.movie_id}/reviews"
        params = {}
        self.assertEqual(self.base.n_requests, 0)
        res = self.base._iter_request(url, **params)
        item = next(res)
        self.assertTrue(inspect.isgenerator(res))
        self.assertIsInstance(item, dict)
        self.assertEqual(self.base.n_requests, 1)

    def test_n_requests(self):
        url_1 = f"https://api.themoviedb.org/3/movie/{self.movie_id}"
        url_2 = f"https://api.themoviedb.org/3/movie/{self.movie_id}/reviews"
        params = {}
        self.assertEqual(self.base.n_requests, 0)
        self.base._request(url_1, **params)
        self.assertEqual(self.base.n_requests, 1)
        self.base._request(url_1, **params)
        self.assertEqual(self.base.n_requests, 2)
        self.base._request(url_1, **params)
        self.assertEqual(self.base.n_requests, 3)
        self.base._iter_request(url_2, **params)
        self.assertEqual(self.base.n_requests, 4)


class MovieTestCase(unittest.TestCase):
    def setUp(self):
        self.movie_id = 18148  # there are tests that depend on the movie id
        self.movie = Movie(self.movie_id)

    def test_repr(self):
        self.assertEqual(self.movie.__repr__(), f"Movie({self.movie_id})")

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
        self.assertIn("US", self.show.title)

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

    def test_repr(self):
        self.assertEqual(self.person.__repr__(), f"Person({self.person_id})")

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


class CompanyTestCase(unittest.TestCase):
    def setUp(self):
        self.company_id = 1
        self.company = Company(self.company_id)

    def test_repr(self):
        self.assertEqual(self.company.__repr__(), f"Company({self.company_id})")

    def test_name_attr(self):
        self.assertIsInstance(self.company.name, str)

    def test_also_known_as_attr(self):
        self.assertIsInstance(self.company.also_known_as, list)

    def test_description_attr(self):
        self.assertIsInstance(self.company.description, str)

    def test_homepage_attr(self):
        self.assertIsInstance(self.company.homepage, str)

    def test_country_attr(self):
        self.assertIsInstance(self.company.country, (Country, type(None)))

    def test_parent_company_attr(self):
        self.assertIsInstance(self.company.parent_company, (str, type(None)))

    def test_logos_attr(self):
        self.assertIsInstance(self.company.logos, list)
        self.assertIsInstance(self.company.logos[0], Image)

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
            _ = Image(self.data)

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
            _ = Credit()

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
