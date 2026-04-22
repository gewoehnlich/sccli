from core.requests.soundcloud_request import SoundcloudRequest


class FetchTrackStreamsRequest(SoundcloudRequest):
    def __init__(
        self,
        access_token: str,
        track_urn: str,
    ) -> None:
        super().__init__(
            method="GET",
            url=self.SOUNDCLOUD_API_LINK + f"/tracks/{track_urn}/streams",
            access_token=access_token,
        )
