import json
from urllib.parse import urlencode, urljoin
from urllib.request import Request, urlopen


def GET_total_pages_for(url, params):
    first_page = GET(url, page=1, **params)
    return first_page["total_pages"]


def GET(url, **params):
    params = urlencode({**params})
    with urlopen(f"{url}?{params}") as response:
        return json.loads(response.read().decode("utf-8"))


def GET_pages(url, params):
    for page in range(1, GET_total_pages_for(url, params) + 1):
        yield from GET(url, page=page, **params)["results"]


def POST(url, data, **params):
    headers = {"content-type": "application/json"}
    data = json.dumps(data).encode("utf-8")
    params = urlencode(params)
    request = Request(f"{url}?{params}", headers=headers, data=data)
    with urlopen(request) as response:
        return json.loads(response.read().decode("utf-8"))


def DELETE(url, data, **params):
    headers = {"content-type": "application/json"}
    data = json.dumps(data).encode("utf-8")
    url = f"{url}?{urlencode(params)}"
    request = Request(url, headers=headers, data=data, method="DELETE")
    with urlopen(request) as response:
        return json.loads(response.read().decode("utf-8"))
