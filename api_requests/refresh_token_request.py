from core.request import Request
from domain.enums.soundcloud_api_endpoint_enum import SoundcloudApiEndpointEnum


class RefreshTokenRequest(Request):
    def __init__(
        self,
        client_id: str,
        client_secret: str,
        refresh_token: str,
    ) -> None:
        super().__init__(
            method="POST",
            url=SoundcloudApiEndpointEnum.TOKEN.value,
            data={
                "grant_type": "refresh_token",
                "client_id": client_id,
                "client_secret": client_secret,
                "refresh_token": refresh_token,
            },
        )
