BASE = "https://api.themoviedb.org"
V = "3"


ACCOUNT_DETAILS = f"{BASE}/{V}/account"
ACCOUNT_CREATED_LISTS = f"{ACCOUNT_DETAILS}/{{account_id}}/lists"
ACCOUNT_FAVORITE_MOVIES = f"{ACCOUNT_DETAILS}/{{account_id}}/favorite/movies"
ACCOUNT_FAVORITE_SHOWS = f"{ACCOUNT_DETAILS}/{{account_id}}/favorite/tv"
ACCOUNT_MARK_AS_FAVORITE = f"{ACCOUNT_DETAILS}/{{account_id}}/favorite"
ACCOUNT_RATED_MOVIES = f"{ACCOUNT_DETAILS}/{{account_id}}/rated/movies"
ACCOUNT_RATED_SHOWS = f"{ACCOUNT_DETAILS}/{{account_id}}/rated/tv"
ACCOUNT_RATED_EPISODES = f"{ACCOUNT_DETAILS}/{{account_id}}/rated/tv/episodes"
ACCOUNT_MOVIE_WATCHLIST = f"{ACCOUNT_DETAILS}/{{account_id}}/watchlist/movies"
ACCOUNT_SHOW_WATCHLIST = f"{ACCOUNT_DETAILS}/{{account_id}}/watchlist/tv"
ACCOUNT_ADD_TO_WATCHLIST = f"{ACCOUNT_DETAILS}/{{account_id}}/watchlist"


AUTH_GUEST_SESSION = f"{BASE}/{V}/authentication/guest_session/new"
AUTH_NEW_TOKEN = f"{BASE}/{V}/authentication/token/new"
AUTH_NEW_SESSION = f"{BASE}/{V}/authentication/session/new"
AUTH_VALIDATE_WITH_LOGIN = (
    f"{BASE}/{V}/authentication/token/validate_with_login"
)
AUTH_DELETE_SESSION = f"{BASE}/{V}/authentication/session"


SEARCH_MOVIE = f"{BASE}/{V}/search/movie"
SEARCH_SHOW = f"{BASE}/{V}/search/tv"
SEARCH_PERSON = f"{BASE}/{V}/search/person"
SEARCH_COMPANY = f"{BASE}/{V}/search/company"


DISCOVER_MOVIES = f"{BASE}/{V}/discover/movie"
DISCOVER_SHOWS = f"{BASE}/{V}/discover/tv"


FIND = f"{BASE}/{V}/find/{{external_id}}"


MOVIE_CERTIFICATION = f"{BASE}/{V}/certification/movie/list"
SHOW_CERTIFICATION = f"{BASE}/{V}/certification/tv/list"
IMAGE_CONFIGURATION = f"{BASE}/{V}/configuration"
COUNTRIES_CONFIGURATION = f"{BASE}/{V}/configuration/countries"
JOBS_CONFIGURATION = f"{BASE}/{V}/configuration/jobs"
LANGUAGES_CONFIGURATION = f"{BASE}/{V}/configuration/languages"
PRIMARY_TRANSLATIONS_CONFIGURATION = (
    f"{BASE}/{V}/configuration/primary_translations"
)
TIMEZONES_CONFIGURATION = f"{BASE}/{V}/configuration/timezones"


MOVIE_DETAILS = f"{BASE}/{V}/movie/{{movie_id}}"
MOVIE_ALTERNATIVE_TITLES = f"{MOVIE_DETAILS}/alternative_titles"
MOVIE_CHANGES = f"{MOVIE_DETAILS}/changes"
MOVIE_CREDITS = f"{MOVIE_DETAILS}/credits"
MOVIE_EXTERNAL_IDS = f"{MOVIE_DETAILS}/external_ids"
MOVIE_IMAGES = f"{MOVIE_DETAILS}/images"
MOVIE_KEYWORDS = f"{MOVIE_DETAILS}/keywords"
MOVIE_RELEASE_DATES = f"{MOVIE_DETAILS}/release_dates"
MOVIE_VIDEOS = f"{MOVIE_DETAILS}/videos"
MOVIE_TRANSLATIONS = f"{MOVIE_DETAILS}/translations"
MOVIE_RECOMMENDATIONS = f"{MOVIE_DETAILS}/recommendations"
MOVIE_SIMILAR = f"{MOVIE_DETAILS}/similar"
MOVIE_REVIEWS = f"{MOVIE_DETAILS}/reviews"
MOVIE_LISTS = f"{MOVIE_DETAILS}/lists"
RATE_MOVIE = f"{MOVIE_DETAILS}/rating"
DELETE_MOVIE_RATING = f"{MOVIE_DETAILS}/rating"
ALL_MOVIE_SECOND_SUFFIXES = [
    "alternative_titles",
    "changes",
    "credits",
    "external_ids",
    "images",
    "keywords",
    "release_dates",
    "videos",
    "translations",
    "recommendations",
    "similar",
    "reviews",
    "lists",
]


SHOW_DETAILS = f"{BASE}/{V}/tv/{{show_id}}"
SHOW_ALTERNATIVE_TITLES = f"{SHOW_DETAILS}/alternative_titles"
SHOW_CHANGES = f"{SHOW_DETAILS}/changes"
SHOW_CONTENT_RATINGS = f"{SHOW_DETAILS}/content_ratings"
SHOW_CREDITS = f"{SHOW_DETAILS}/credits"
SHOW_EPISODE_GROUPS = f"{SHOW_DETAILS}/episode_groups"
SHOW_EXTERNAL_IDS = f"{SHOW_DETAILS}/external_ids"
SHOW_IMAGES = f"{SHOW_DETAILS}/images"
SHOW_KEYWORDS = f"{SHOW_DETAILS}/keywords"
SHOW_RECOMMENDATIONS = f"{SHOW_DETAILS}/recommendations"
SHOW_REVIEWS = f"{SHOW_DETAILS}/reviews"
SHOW_SCREENED_THEATRICALLY = f"{SHOW_DETAILS}/screened_theatrically"
SHOW_SIMILAR = f"{SHOW_DETAILS}/similar"
SHOW_TRANSLATIONS = f"{SHOW_DETAILS}/translations"
SHOW_VIDEOS = f"{SHOW_DETAILS}/videos"
RATE_SHOW = f"{SHOW_DETAILS}/rating"
DELETE_SHOW_RATING = f"{SHOW_DETAILS}/rating"
ALL_SHOW_SECOND_SUFFIXES = [
    "alternative_titles",
    "changes",
    "content_ratings",
    "credits",
    "episode_groups",
    "external_ids",
    "images",
    "keywords",
    "recommendations",
    "reviews",
    "screened_theatrically",
    "similar",
    "translations",
    "videos",
]


PERSON_DETAILS = f"{BASE}/{V}/person/{{person_id}}"
PERSON_CHANGES = f"{PERSON_DETAILS}/changes"
PERSON_MOVIE_CREDITS = f"{PERSON_DETAILS}/movie_credits"
PERSON_SHOW_CREDITS = f"{PERSON_DETAILS}/tv_credits"
PERSON_COMBINED_CREDITS = f"{PERSON_DETAILS}/combined_credits"
PERSON_EXTERNAL_IDS = f"{PERSON_DETAILS}/external_ids"
PERSON_IMAGES = f"{PERSON_DETAILS}/images"
PERSON_TAGGED_IMAGES = f"{PERSON_DETAILS}/tagged_images"
PERSON_TRANSLATIONS = f"{PERSON_DETAILS}/translations"
ALL_PERSON_SECOND_SUFFIXES = [
    "changes",
    "movie_credits",
    "tv_credits",
    "combined_credits",
    "external_ids",
    "images",
    "tagged_images",
    "translations",
]

SEASON_DETAILS = f"{BASE}/{V}/tv/{{show_id}}/season/{{season_number}}"
SEASON_CHANGES = f"{BASE}/{V}/tv/season/{{season_id}}/changes"
SEASON_CREDITS = f"{SEASON_DETAILS}/credits"
SEASON_EXTERNAL_IDS = f"{SEASON_DETAILS}/external_ids"
SEASON_IMAGES = f"{SEASON_DETAILS}/images"
SEASON_VIDEOS = f"{SEASON_DETAILS}/videos"
ALL_SEASON_SECOND_SUFFIXES = ["credits", "external_ids", "images", "videos"]


EPISODE_DETAILS = f"{BASE}/{V}/tv/{{show_id}}/season/{{season_number}}/episode/{{episode_number}}"
EPISODE_CHANGES = f"{BASE}/{V}/tv/{{episode_id}}/changes"
EPISODE_CREDITS = f"{EPISODE_DETAILS}/credits"
EPISODE_EXTERNAL_IDS = f"{EPISODE_DETAILS}/external_ids"
EPISODE_TRANSLATIONS = f"{EPISODE_DETAILS}/translations"
EPISODE_IMAGES = f"{EPISODE_DETAILS}/images"
EPISODE_VIDEOS = f"{EPISODE_DETAILS}/videos"
ALL_EPISODE_SECOND_SUFFIXES = [
    "credits",
    "external_ids",
    "translations",
    "images",
    "videos",
]

PERSON_DETAILS = f"{BASE}/{V}/person/{{person_id}}"
PERSON_CHANGES = f"{PERSON_DETAILS}/changes"
PERSON_MOVIE_CREDITS = f"{PERSON_DETAILS}/movie_credits"
PERSON_SHOW_CREDITS = f"{PERSON_DETAILS}/tv_credits"
PERSON_COMBINED_CREDITS = f"{PERSON_DETAILS}/combined_credits"
PERSON_EXTERNAL_IDS = f"{PERSON_DETAILS}/external_ids"
PERSON_IMAGES = f"{PERSON_DETAILS}/images"
PERSON_TAGGED_IMAGES = f"{PERSON_DETAILS}/tagged_images"
PERSON_TRANSLATIONS = f"{PERSON_DETAILS}/translations"
ALL_PERSON_SECOND_SUFFIXES = [
    "changes",
    "movie_credits",
    "tv_credits",
    "combined_credits",
    "external_ids",
    "images",
    "tagged_images",
    "translations",
]


COMPANY_DETAILS = f"{BASE}/{V}/company/{{company_id}}"
COMPANY_ALTERNATIVE_NAMES = f"{COMPANY_DETAILS}/alternative_names"
COMPANY_IMAGES = f"{COMPANY_DETAILS}/images"


KEYWORD_DETAILS = f"{BASE}/{V}/keyword/{{keyword_id}}"
KEYWORD_MOVIES = f"{KEYWORD_DETAILS}/movies"


MOVIE_GENRES = f"{BASE}/{V}/genre/movie/list"
SHOW_GENRES = f"{BASE}/{V}/genre/tv/list"


CREDIT_DETAILS = f"{BASE}/{V}/credit/{{credit_id}}"


LIST_DETAILS = f"{BASE}/{V}/list/{{list_id}}"
LIST_CHECK_MOVIE_STATUS = f"{LIST_DETAILS}/item_status"
CREATE_LIST = f"{BASE}/{V}/list"
DELETE_LIST = f"{BASE}/{V}/list/{{list_id}}"
ADD_MOVIE_TO_LIST = f"{BASE}/{V}/list/{{list_id}}/add_item"
REMOVE_MOVIE_FROM_LIST = f"{BASE}/{V}/list/{{list_id}}/remove_item"
CLEAR_LIST = f"{BASE}/{V}/list/{{list_id}}/clear"
