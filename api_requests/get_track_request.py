from core.requests.soundcloud_request import SoundcloudRequest


class GetTrackRequest(
    SoundcloudRequest
):
    def __init__(
        self,
        access_token: str,
        track_urn: str,
    ) -> None:
        super().__init__(access_token = access_token)

        self.method = "GET"

        self.url = SOUNDCLOUD_API_LINK + f"/tracks/{track_urn}"
