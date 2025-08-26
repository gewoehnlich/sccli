from requests import Response
from core.request import Request

def send_request(request: Request) -> Response:
    return request.send()
