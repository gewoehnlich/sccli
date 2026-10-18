from core.soundcloud_request import SoundcloudRequest


class AuthenticationRequest(SoundcloudRequest):
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
            url=self.TOKEN_API_ENDPOINT,
            data={
                "grant_type": "authorization_code",
                "client_id": client_id,
                "client_secret": client_secret,
                "redirect_uri": redirect_uri,
                "code_verifier": code_verifier,
                "code": auth_code,
            },
        )
