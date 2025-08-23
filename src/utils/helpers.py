from os import getenv
from pprint import pprint
from requests import Response
from src.core.request import Request

def safe_getenv(key: str) -> str:
    value = getenv(key)
    if not value:
        raise ValueError(f"{key} is not set in .env file.")

    return value

def send_request(request: Request) -> Response:
    return request.send()

def print_response(response: Response) -> None:
    pprint(response.status_code)
    pprint(response.headers)
    pprint(response.url)
    pprint(response.json())
