import json
from urllib.parse import urljoin, urlencode
from urllib.request import urlopen


def get_response(url, **params):
    params = urlencode({**params})
    response = urlopen(f"{url}?{params}")
    return json.loads(response.read().decode("utf-8"))


def get_total_pages_for(url, params):
    first_page = get_response(url, page=1, **params)
    return first_page["total_pages"]


def search_results_for(url: str, params: dict):
    for page in range(1, get_total_pages_for(url, params) + 1):
        yield from get_response(url, page=page, **params)["results"]
