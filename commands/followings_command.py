from requests_.followings_request import FollowingsRequest
from requests import Response
from pprint import pprint
from utils.send_request import send_request
from typing import List

def followings_command(args: List[str]) -> None:
    response: Response = send_request(FollowingsRequest())
    pprint(response.json())
