
BASEURL = "https://api.themoviedb.org/"
SEARCH_MOVIE_SUFFIX = "3/search/movie"
SEARCH_SHOW_SUFFIX = "3/search/tv"
SEARCH_PERSON_SUFFIX = "3/search/person"
SEARCH_COMPANY_SUFFIX = "3/search/company"
DISCOVER_MOVIES_SUFFIX = "3/discover/movie"
DISCOVER_SHOWS_SUFFIX = "3/discover/tv"

MOVIE_DETAILS_SUFFIX = "3/movie/{}" # {movie_id}
MOVIE_ALTERNATIVE_TITLES_SUFFIX = "3/movie/{}/alternative_titles"
MOVIE_CHANGES_SUFFIX = "3/movie/{}/changes"
MOVIE_CREDITS_SUFFIX = "3/movie/{}/credits"
MOVIE_EXTERNAL_IDS_SUFFIX = "3/movie/{}/external_ids"
MOVIE_IMAGES_SUFFIX = "3/movie/{}/images"
MOVIE_KEYWORDS_SUFFIX = "3/movie/{}/keywords"
MOVIE_RELEASE_DATES_SUFFIX = "3/movie/{}/release_dates"
MOVIE_VIDEOS_SUFFIX = "3/movie/{}/videos"
MOVIE_TRANSLATIONS_SUFFIX = "3/movie/{}/translations"
MOVIE_RECOMMENDATIONS_SUFFIX = "3/movie/{}/recommendations"
MOVIE_SIMILAR_SUFFIX = "3/movie/{}/similar"
MOVIE_REVIEWS_SUFFIX = "3/movie/{}/reviews"
MOVIE_LISTS_SUFFIX = "3/movie/{}/lists"
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

SHOW_DETAILS_SUFFIX = "3/tv/{}" # {tv_id}
SHOW_ALTERNATIVE_TITLES_SUFFIX = "3/tv/{}/alternative_titles"
SHOW_CHANGES_SUFFIX = "3/tv/{}/changes"
SHOW_CONTENT_RATINGS_SUFFIX = "3/tv/{}/content_ratings"
SHOW_CREDITS_SUFFIX = "3/tv/{}/credits"
SHOW_EPISODE_GROUPS_SUFFIX = "3/tv/{}/episode_groups"
SHOW_EXTERNAL_IDS_SUFFIX = "3/tv/{}/external_ids"
SHOW_IMAGES_SUFFIX = "3/tv/{}/images"
SHOW_KEYWORDS_SUFFIX = "3/tv/{}/keywords"
SHOW_RECOMMENDATIONS_SUFFIX = "3/tv/{}/recommendations"
SHOW_REVIEWS_SUFFIX = "3/tv/{}/reviews"
SHOW_SCREENED_THEATRICALLY_SUFFIX = "3/tv/{}/screened_theatrically"
SHOW_SIMILAR_SUFFIX = "3/tv/{}/similar"
SHOW_TRANSLATIONS_SUFFIX = "3/tv/{}/translations"
SHOW_VIDEOS_SUFFIX = "3/tv/{}/videos"
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