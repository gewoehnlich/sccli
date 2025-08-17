from src.requests.following_request import FollowingRequest
from requests import Response
from pprint import pprint
from src.utils.helpers import send_request
from typing import List

def following_command(args: List[str]) -> None:
    response: Response = send_request(FollowingRequest())
    pprint(response.json())
