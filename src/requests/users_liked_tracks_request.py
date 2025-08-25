from src.core.request import Request
from src.utils.links import SOUNDCLOUD_API_LINK
from src.utils.access_token import access_token

class UsersLikedTracksRequest(Request):
    _API_ENDPOINT: str = "/me/likes/tracks"

    def __init__(
        self,
        url: str | None = None,
    ) -> None:
        super().__init__(
            access_token = access_token()
        )

        self.method = "GET"

        self.url = SOUNDCLOUD_API_LINK + self._API_ENDPOINT

        if url:
            self.url = url

        self.params["limit"] = "1"
        self.params["access"] = "playable"
        self.params["linked_partitioning"] = "true"
