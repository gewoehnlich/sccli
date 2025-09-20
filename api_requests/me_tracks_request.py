from core.requests.soundcloud_request import SoundcloudRequest


class MeTracksRequest(
    SoundcloudRequest
):
    def __init__(
        self,
        access_token: str,
    ) -> None:
        super().__init__(
            access_token = access_token
        )

        self.method = "GET"

        self.url = self.SOUNDCLOUD_API_LINK + '/me/tracks'

        self.params["limit"] = "5"
        self.params["linked_partitioning"] = "true"
