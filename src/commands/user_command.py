from src.requests.user_info_request import UserInfoRequest
import requests
from pprint import pprint

def user_command() -> None:
    request: UserInfoRequest = UserInfoRequest()
    response: requests.response = request.send()
    pprint(response.json())
