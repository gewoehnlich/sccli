from src.core.auth import Auth
from src.core.request import Request
from src.utils.links import SOUNDCLOUD_API_LINK

class FollowingsTracksRequest(Request):
    def __init__(self) -> None:
        access_token: str = Auth().get_access_token()
        super().__init__(access_token)

        self.url = SOUNDCLOUD_API_LINK + '/me/followings/tracks'
