from core.requests.soundcloud_request import SoundcloudRequest


class FetchTrackFromStreamingUrlRequest(SoundcloudRequest):
    def __init__(
        self,
        access_token: str,
        url: str,
    ) -> None:
        super().__init__(
            method="GET",
            url=url,
            access_token=access_token,
        )
