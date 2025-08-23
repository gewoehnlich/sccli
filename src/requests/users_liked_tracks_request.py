from src.core.request import Request
from src.utils.links import SOUNDCLOUD_API_LINK
from src.utils.access_token import access_token

class UsersLikedTracksRequest(Request):
    def __init__(self) -> None:
        super().__init__(access_token = access_token())

        self.method = "GET"

        self.url = SOUNDCLOUD_API_LINK + '/me/likes/tracks'
