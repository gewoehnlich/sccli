from src.requests.users_liked_tracks_request import UsersLikedTracksRequest 
from requests import Response
from pprint import pprint

def users_liked_tracks_command() -> None:
    response: Response = UsersLikedTracksRequest().send()
    pprint(response.json())
