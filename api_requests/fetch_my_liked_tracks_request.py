from core.requests.soundcloud_request import SoundcloudRequest


class FetchMyLikedTracksRequest(SoundcloudRequest):
    def __init__(
        self,
        access_token: str,
        url: str | None = None,
    ) -> None:
        super().__init__(
            access_token=access_token,
        )

        self.method = "GET"

        if url:
            self.url = url
        else:
            self.url = self.SOUNDCLOUD_API_LINK + "/me/likes/tracks"

        self.params["limit"] = "1"
        self.params["access"] = "playable"
        self.params["linked_partitioning"] = "true"
