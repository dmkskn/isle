# THE MOVIE DATABASE PYTHON WRAPPER

[![Build Status](https://travis-ci.org/dmkskn/isle.svg?branch=master)](https://travis-ci.org/dmkskn/isle)

`isle` is a clear and distinct wrapper for The Movie Database API.

## TABLE OF CONTENTS

- [REQUIREMENTS](#REQUIREMENTS)
- [INSTALLATION](#INSTALLATION)
- [TMDB API KEY](#TMDB-API-KEY)
- [FUNCTIONS](#FUNCTIONS)
- [OBJECTS](#OBJECTS)
- [ACCOUNT](#ACCOUNT)

## REQUIREMENTS

- **Python 3.6+**
- **No dependencies** other than the standard library

## INSTALLATION

Using `pip`:

```python
pip install isle
```

## TMDB API KEY

Export your TMDb API key as an environment variable:

```bash
$ export TMDB_API_KEY='YOUR_API_KEY'
```

Or set the `TMDB_API_KEY` variable:

```python
import isle

isle.TMDB_API_KEY = 'YOUR_API_KEY'
```

## FUNCTIONS

### Search
Search functions look for movies, TV shows, people or companies by their names or titles.

All search functions are *generators*.

```python
>>> import inspect
>>> import isle

>>> inspect.isgenerator(isle.search_movie)
True

>>> inspect.isgenerator(isle.search_show)
True

>>> # and so on.
```

#### `isle.search_movie(query: str, **kwargs)`

Searches for movies. It generates `Movie` instances.

Let's search for Ozu's "Tokyo Story":

```python
>>> for movie in isle.search_movie("Tokyo Story"):
...     print(movie)

Movie(18148)
Movie(528533)
...
Movie(104343)
```

Let's get only the first result:

```python
>>> tokyo_story = next(isle.search_movie("Tokyo Story", year=1953))

>>> tokyo_story
Movie(18148)
```

There are several keyword arguments:

 - `year` — filters a movie by release year
 - `region` — filters release dates. Must be an ISO 3166-1 code (uppercase).
 - `include_adults` — chooses whether to inlcude adult (pornography) content in the results (bool).
 - `language` — displays translated data for the fields that support it (some default values in `Movie` object). Must be an ISO 639-1 code.


#### `isle.search_show(query: str, **kwargs)`

Searches for a TV show. It generates `Show` instances.

```python
>>> castle_rock = next(isle.search_show("Castle Rock"))

>>> castle_rock
Show(71116)
```
There is a keyword argument `first_air_date_year`, which can be specified for more accurate results.

#### `isle.search_person(query: str, **kwargs)`

Searches for people. It generates `Person` instances.

```python
>>> john_cassavetes = next(isle.search_person("John Cassavetes"))

>>> john_cassavetes
Person(11147)
```

There are `language`, `region` and `include_adults` keyword arguments (see the part about `search_movie` above to understand what they change).

#### `isle.search_company(query: str, **kwargs)`

Searches for companies. It generates `Company` instances.

```python
>>> lucasfilm_company = next(isle.search_company("Lucasfilm"))

>>> lucasfilm_company
Company(1)
```

### Discover

Like search functions, all discover functions are also *generators*. But instead of searching by name or title, these ones descover movies or TV shows by different types of data like average rating, number of votes, genres and certifications.

> To understand `options`, you need to read [this](https://developers.themoviedb.org/3/discover/movie-discover) and [this](https://developers.themoviedb.org/3/discover/tv-discover).

#### `isle.discover_movies(options: dict)`

Discovers movies by different types of data.

Let's discover the first 3 movies with Jason Schwartzman:

```python
>>> from itertools import islice

>>> schwartzman = next(isle.search_person("Jason Schwartzman"))

>>> options = {
    "sort_by": "release_date.asc",
    "with_cast": schwartzman.tmdb_id
}

>>> for movie in islice(isle.discover_movies(options), 3):
...     print(f"'{movie.year} - {movie.title['original']}'")

'1998 - Rushmore'
'2001 - CQ'
'2002 - Slackers'
```

#### `isle.discover_shows(options: dict)`

Discovers TV shows by different types of data. It works like `discover_movies`, but note that the options are different.

Let's discover top 3 most popular TV shows on TMDb:

```python
>>> options = {'sort_by': 'popularity.desc'}

>>> for show in islice(isle.discover_shows(options), 3):
...     print(f"'{show.vote.average:<10} {show.title['original']}'")

'8         ドラゴンボール'
'6.7       The Flash'
'6.8       The Big Bang Theory'
```

### Find

#### `isle.find(external_id: str, *, src: str, **options)`

The `find` function searches for objects (movies, TV shows and people) by an external ID (for example, an IMDb ID). It returns the results in a single response.

```python
>>> results = tmdb.find("tt0053604", src="imdb_id")

>>> results
{'movie_results': [Movie(284)], 'person_results': [], 'tv_results': []}
```

### Others

Other functions return some general information, such as genres, languages, time zones supported in TMDb.

Let's just list them all (you always can use the build-in `help` function to see more information):

- `isle.get_movie_certifications(country=None)`
- `isle.get_show_certifications(country=None)`
- `isle.get_movie_genres(objects=False)`
- `isle.get_show_genres(objects=False)`
- `isle.get_image_configurations()`
- `isle.get_countries(objects=False)`
- `isle.get_jobs()`
- `isle.get_languages(objects=False)`
- `isle.get_primary_translations()`
- `isle.get_timezones()`

## OBJECTS

Let's take a close look at `Movie`, `Show`, `Person` and `Company` objects.

- They can be initialized by a TMDb ID or obtained by *search* and *discover* functions (as we see above).

- They can be used in two different ways: use *methods* that return raw responses or use *properties* that enrich objects with more functionality (you'll see this below)

### `Movie`

Represents a movie. It can be initialized with a TMDb ID.

```python
>>> movie = isle.Movie(18148)
```

Now the `movie` doesn't contain any data except the ID. It hasn't made any requests to the API yet (You can see how many requests were made by the `n_requests` attribute).

```python
>>> movie.data
{'id': 18148}

>>> movie.n_requests
0
```

#### Methods
`Movie` (as well as other objects, such as `Show`, `Person` or `Company`) has `get_<something>` and `iter_<something>` methods. Let's list them:

- `get_all()`
- `get_alternative_titles()`
- `get_changes()`
- `get_credits()`
- `get_details()`
- `get_external_ids()`
- `get_images()`
- `get_keywords()`
- `get_release_dates()`
- `get_translations()`
- `get_videos()`
- `iter_lists()`
- `iter_recommendations()`
- `iter_reviews()`
- `iter_similar_movies()`

Each method makes only *one* request to the API. That's why the best practice is  to use `get_all()` method instead of calling several other methods. So instead of doing the following:

```python
>>> movie = isle.Movie(18148)

>>> credits = movie.get_credits() # making first request

>>> movie.n_requests
1

>>> keywords = movie.get_keywords()  # making second request

>>> movie.n_requests
2
```

Do this:

```python
>>> movie = isle.Movie(18148)

>>> movie.n_requests
0

>>> all_data = movie.get_all() # making first request

>>> movie.n_requests
1

>>> credits, keywords = all_data["credits"], all_data["keywords"]

>>> movie.n_requests
1
```

All the received data is saved in the `data` attribute. Now it contains all the data, because we've called the `get_all()` method.

```python
>>> all_data == movie.data
True

>>> keywords == movie.data["keywords"]
True
```

All the data received with methods is structured in the same way as in the [raw](https://developers.themoviedb.org/3/movies/get-movie-details) API responses.

#### Properties ☝️

Another way to get data is to use properties (it is actually the best way).

Let's see an example. What if you need to get the titles of a movie in different languages? You can call `get_all()` and retrieve the titles from the `data` attribute:

```python
>>> movie.get_all()

>>> acc = {}

>>> acc["original"] = movie.data["original_title"]

>>> acc["default"] = movie.data["title"]

>>> for item in movie.data["translations"]["translations"]:
...    acc[item["iso_3166_1"]] = item["data"]["title"]

>>> acc
{'original': '東京物語', 'default': 'Tokyo Story', 'RU': 'Токийская повесть', 'US': 'Tokyo Story',  ..., 'FR': 'Voyage à Tokyo'}

```

Or you can just use the `title` property:

```python
>>> movie = isle.Movie(18148)

>>> movie.title
{'original': '東京物語', 'default': 'Tokyo Story', 'RU': 'Токийская повесть', 'US': 'Tokyo Story',  ..., 'FR': 'Voyage à Tokyo'}

>>> movie.n_requests
1
```

In the same way you can use the `overview` property:

```python
>>> movie.overview["FR"]
"Un couple de personnes âgées rend visite à leurs enfants à Tokyo. D'abord reçus avec les égards qui leur sont dûs, ils deviennent bientôt dérangeants dans leur vie quotidienne."
```

When a property is called, it searches for the required data in the `data` attribute and if there is no such data, it calls `get_all()` behind the scenes. After calling the `title` attribute, all the raw data is downloaded to the `data` attribute.

```python
>>> movie.genres
[Genre(tmdb_id=18, name='Drama')] # Genre is a `NamedTuple` object

>>> person, credit = movie.crew[0]
>>> person.name, credit.job
('Yasujirō Ozu', 'Director')

>>> person, credit = movie.cast[0]
>>> person.name, credit.job, credit.character
('Chishū Ryū', 'Actor', 'Shukishi Hirayama')

>>> movie.vote
Vote(average=8.3, count=292) # It is a `NamedTuple` object too

>>> movie.releases["US"]
[{'certification': '', 'type': 3, 'date': '1972-03-13T00:00:00.000Z', 'note': ''}]

>>> movie.n_requests
1
```

When `search_movie` and `discover_movie` functions return `Movie` instances, they add initial data to the `data` atributes.

```python
>>> tokyo_story = next(isle.search_movie("Tokyo Story", year=1953))

>>> tokyo_story.n_requests
0

>>> tokyo_story.year
1953

>>> tokyo_story.is_adult
False

>>> tokyo_story.popularity
5.816

>>> tokyo_story.n_requests # it did not make API requests yet
0

>>> # but
>>> person, credit = tokyo_story.crew[0]
>>> tokyo_story.n_requests
1
```

In the same way, `Movie` adds some initial data to the `data` attribute of `Person` and `Company` instances:

```python
>>> person, _ = tokyo_story.crew[0]

>>> person.name
'Yasujirō Ozu'

>>> person.n_requests
0

>>> company = tokyo_story.companies[0]
>>> company.name
'Shochiku Co., Ltd.'

>>> company.n_requests
0
```

Use the build-in `help` function to see all available properties.

### `Show`, `Person` and `Company`

These objects are similar to `Movie`. They also have `get_<something>` and `iter_<something>` methods and properties that do all the routine work.

The main difference is that `Company` doesn't have the `get_all()` method, so, behind the scenes, it can call several `get` methods (though the main information is returned by `get_details()`).

```python
>>> company = Company(1)

>>> company.name
'Lucasfilm'

>>> company.homepage
'http://www.lucasfilm.com'

>>> company.n_requests
1

>>> company.logos # searches for images and calls `get_images` if there are no images in the `data` attribute
[Image(heigh=99, width=295, _type=logo)]

>>> company.n_requests
2

>>> company.also_known_as # searches for alternative_names and calls `get_alternative_names` if there are no names in the `data` attribute
[]

>>> company.n_requests
3
```

### `Season`, `Episode`, `Credit` and others

A `Season` is returned by a `Show` (and  an `Episode` is returned by `Season`). These ones and `Credit` are also similar to the main objects above.

```python
>>> show = next(isle.search_show("Castle Rock"))
```

Season:

```python
>>> season = show.seasons[0]

>>> all_raw_data = season.get_all()

>>> season.n_requests
1
```

Episode:

```python
>>> season.title
'Season 1'

>>> episode = season.episodes[0]

>>> f"{episode.n} episode of {episode.sn} season"
'1 episode of 1 season'

>>> episode.title['US']
'Severance'

>>> episode.n_requests
1
```

Credit:

```python
>>> person, credit = episode.crew[0]

>>> credit
Credit(5b6192b09251414064012485)

>>> credit.department, credit.job
('Directing', 'Director')

>>> person.name == credit.person.name
True
```

There are a few objects such as `Language`, `Country`, `Genre`, `Keyword` and `Vote`. They are just [`NamedTuple`](https://docs.python.org/3/library/typing.html#typing.NamedTuple)-like objects.

```python
>>> movie = isle.Movie(18148)

>>> isinstance(movie.vote, tuple)
True

>>> movie.vote[0] == movie.vote.average
True
```

And there is an `Image`. It contains attributes which are the same as in the [raw dict](https://developers.themoviedb.org/3/movies/get-movie-images): `aspect_ratio`, `file_path`, `width`, `height`, etc. And the property `url` that makes a request to the TMDb API for [image configurations](https://developers.themoviedb.org/3/configuration/get-api-configuration) and returns `dict` with full URLs to the image.

```python
>>> poster = movie.posters[0]

>>> poster.height poster.width, poster.file_path
(952, 666, '/3Zu3MojWSaV3rt5gX5fFdDO3GoF.jpg')

>>> poster.url['original']
'https://image.tmdb.org/t/p//original/3Zu3MojWSaV3rt5gX5fFdDO3GoF.jpg'

>>> set(poster.sizes) == poster.url.keys()
True
```

## ACCOUNT

To get started with a TMDb user account, create an instance of `Account` and log in with a user name and password:

```python
>>> import os

>>> account = isle.Account()

>>> account.login(os.getenv("TMDB_USERNAME"), os.getenv("TMDB_PASSWORD"))
{'success': True, 'session_id': '7b2578cddffce240f5f3387527761802c0d5c1ef'}
```

Don't try to seek out how to rate a movie inside a `Movie` instance or how to add a new list inside a `List` instance. All that can be done with a user account, can be done by an `Account` instance.

Rate:
```python
>>> account.rate(isle.Movie(18148), 8.5)
{'status_code': 1, 'status_message': 'Success.'}

>>> for movie in account.iter_rated_movies():
...     print(movie)
Movie(18148)

>>> account.delete_rating(isle.Movie(18148))
{'status_code': 13, 'status_message': 'The item/record was deleted successfully.'}
```

Watchlist:
```python
>>> account.add_to_watchlist(isle.Movie(18148))
{'status_code': 1, 'status_message': 'Success.'}

>>> for item in account.iter_movie_watchlist():
...     print(item)
Movie(18148)

>>> account.remove_from_watchlist(isle.Movie(18148))
{'status_code': 13, 'status_message': 'The item/record was deleted successfully.'}
```

And other things:

```python
>>> account.mark_as_favorite(isle.Movie(18148))
{'status_code': 1, 'status_message': 'Success.'}

>>> for movie in account.iter_favorite_movies():
...     print(movie)
Movie(18148)

>>> for l in account.iter_lists():
...     print(l)
List(96926)
```
