from src.requests.users_liked_tracks_request import UsersLikedTracksRequest 
from requests import Response
from pprint import pprint
from src.utils.helpers import send_request
from typing import List

def users_liked_tracks_command(args: List[str]) -> None:
    response: Response = send_request(UsersLikedTracksRequest())
    pprint(response.json())
