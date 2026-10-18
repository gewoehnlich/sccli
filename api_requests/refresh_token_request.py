from core.soundcloud_request import SoundcloudRequest


class RefreshTokenRequest(SoundcloudRequest):
    def __init__(
        self,
        client_id: str,
        client_secret: str,
        refresh_token: str,
    ) -> None:
        super().__init__(
            method="POST",
            url=self.REFRESH_TOKEN_API_ENDPOINT,
            data={
                "grant_type": "refresh_token",
                "client_id": client_id,
                "client_secret": client_secret,
                "refresh_token": refresh_token,
            },
        )
