from src.requests.get_users_liked_tracks_request import GetUsersLikedTracksRequest 
from requests import Response
from pprint import pprint

def get_users_liked_tracks_command() -> None:
    response: Response = GetUsersLikedTracksRequest().send()
    pprint(response.json())
