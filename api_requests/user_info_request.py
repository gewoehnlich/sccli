from core.request import Request
from utils.links import SOUNDCLOUD_API_LINK


class UserInfoRequest(Request):
    def __init__(
        self,
        access_token: str
    ) -> None:
        super().__init__(access_token = access_token)

        self.method = "GET"

        self.url = SOUNDCLOUD_API_LINK + '/me'
