from src.requests.user_info_request import UserInfoRequest
from requests import Response
from pprint import pprint

def user_command() -> None:
    response: Response = UserInfoRequest().send()
    pprint(response.json())
