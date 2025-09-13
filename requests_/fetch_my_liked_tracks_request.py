from core.request import Request
from utils.links import SOUNDCLOUD_API_LINK

class FetchMyLikedTracksRequest(Request):
    _API_ENDPOINT: str = "/me/likes/tracks"

    def __init__(
        self,
        # access_token: str,
        auth,
        url: str | None = None,
    ) -> None:
        super().__init__(
            access_token = auth.get_access_token(),
        )

        self.method = "GET"

        if url:
            self.url = url
        else:
            self.url = SOUNDCLOUD_API_LINK + self._API_ENDPOINT

        self.params["limit"] = "1"
        self.params["access"] = "playable"
        self.params["linked_partitioning"] = "true"
