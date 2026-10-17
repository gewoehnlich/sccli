from core.request import Request
from domain.enums.soundcloud_api_endpoint_enum import SoundcloudApiEndpointEnum


class AuthenticationRequest(Request):
    def __init__(
        self,
        client_id: str,
        client_secret: str,
        redirect_uri: str,
        code_verifier: str,
        auth_code: str,
    ) -> None:
        super().__init__(
            method="POST",
            url=SoundcloudApiEndpointEnum.TOKEN.value,
            data={
                "grant_type": "authorization_code",
                "client_id": client_id,
                "client_secret": client_secret,
                "redirect_uri": redirect_uri,
                "code_verifier": code_verifier,
                "code": auth_code,
            },
        )
