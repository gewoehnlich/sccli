from src.core.auth import Auth
from src.core.request import Request
import requests

class UserInfoRequest(Request):
    def __init__(self) -> None:
        access_token: str = Auth().get_access_token()
        super().__init__(access_token)

        self.url = "https://api.soundcloud.com/me"
        self.data = {}

    def send(self) -> requests.Response:
        response: requests.Response = requests.get(
            url     = self.url, 
            headers = self.headers, 
            data    = self.data
        )

        return response
