from src.actions.get_my_liked_tracks_action import GetMyLikedTracksAction
from src.requests.users_liked_tracks_request import UsersLikedTracksRequest 
from requests import Response
from pprint import pprint
from src.utils.send_request import send_request
from typing import List, Any
from src.requests.next_href_request import NextHrefRequest
from src.utils.run_action import run_action

def users_liked_tracks_command(args: List[str]) -> None:
    result: bool = run_action(
        GetMyLikedTracksAction()
    )
    # to-do: handle true / false
