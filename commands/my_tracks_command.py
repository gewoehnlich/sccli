from requests_.me_tracks_request import MeTracksRequest 
from core.request import Request
from requests import Response
from pprint import pprint
from utils.send_request import send_request
from typing import List

def my_tracks_command(args: List[str]) -> None:
    request: Request = MeTracksRequest()
    response: Response = send_request(request = request)
    pprint(response.json())
