from core.requests.soundcloud_request import SoundcloudRequest


class FollowingsRequest(
    SoundcloudRequest
):
    def __init__(
        self,
        access_token: str,
    ) -> None:
        super().__init__(access_token = access_token)

        self.method = "GET"

        self.url = self.SOUNDCLOUD_API_LINK + '/me/followings'
