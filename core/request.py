import requests


class Request(
    requests.Request
):
    method:  str = str()
    url:     str = str()
    headers: dict[str, str] = {
        "Accept": "application/json; charset=utf-8",
        "Content-Type": "application/x-www-form-urlencoded",
    }
    params: dict[str, str] = {}
    data:   dict[str, str] = {}
