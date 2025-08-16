from src.requests.user_info_request import UserInfoRequest
from requests import Response
from pprint import pprint
from src.utils.helpers import send_request

def user_command() -> None:
    # response: Response = UserInfoRequest().send()
    response: Response = send_request(UserInfoRequest)
    pprint(response.json())
