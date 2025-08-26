from requests_.user_info_request import UserInfoRequest
from requests import Response
from pprint import pprint
from utils.send_request import send_request

def user_command() -> None:
    response: Response = send_request(UserInfoRequest())
    pprint(response.json())
