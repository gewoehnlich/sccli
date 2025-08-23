from requests import Response
from src.core.request import Request

def send_request(request: Request) -> Response:
    return request.send()
