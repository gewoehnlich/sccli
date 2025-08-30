from requests_.followings_tracks_request import FollowingsTracksRequest
from requests import Response
from pprint import pprint
from utils.send_request import send_request
from typing import List

def followings_tracks_command(self, args: List[str]) -> None:
    response: Response = send_request(FollowingsTracksRequest())
    pprint(response.json())
