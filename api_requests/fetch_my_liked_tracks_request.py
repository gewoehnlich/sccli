from core.auth import Auth
from core.dto import Dto
from core.requests.soundcloud_request import SoundcloudRequest


class FetchMyLikedTracksRequest(
    SoundcloudRequest
):
    def __init__(
        self,
        auth: Auth,
        dto: Dto,
        url: str | None = None,
    ) -> None:
        super().__init__(
            access_token = auth.get_access_token(),
        )

        self.method = "GET"

        if url:
            self.url = url
        else:
            self.url = self.SOUNDCLOUD_API_LINK + "/me/likes/tracks"

        self.params["limit"] = "1"
        self.params["access"] = "playable"
        self.params["linked_partitioning"] = "true"
