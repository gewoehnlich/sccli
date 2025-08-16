from src.core.auth import Auth
from src.core.request import Request
from src.utils.links import SOUNDCLOUD_API_LINK
import requests

class GetUsersLikedTracksRequest(Request):
    def __init__(self) -> None:
        access_token: str = Auth().get_access_token()
        super().__init__(access_token)

        self.url = SOUNDCLOUD_API_LINK + '/me/likes/tracks'
        self.data = {}

    def send(self) -> requests.Response:
        response: requests.Response = requests.get(
            url     = self.url, 
            headers = self.headers, 
            data    = self.data
        )

        return response
