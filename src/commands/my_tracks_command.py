from src.requests.me_tracks_request import MeTracksRequest 
from requests import Response
from pprint import pprint
from src.utils.helpers import send_request
from typing import List

def my_tracks_command(args: List[str]) -> None:
    response: Response = send_request(MeTracksRequest())
    pprint(response.json())
