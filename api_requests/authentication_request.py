from core.dto import Dto
from core.requests.auth_request import AuthRequest


class AuthenticationRequest(
    AuthRequest
):
    def __init__(
        self,
        client_id:     str,
        client_secret: str,
        redirect_uri:  str,
        code_verifier: str,
        auth_code:     str,
        dto: Dto,
    ) -> None:
        super().__init__()

        self.method = "POST"

        self.url = "https://secure.soundcloud.com/oauth/token"

        self.data = {
            "grant_type":    "authorization_code",
            "client_id":     client_id,
            "client_secret": client_secret,
            "redirect_uri":  redirect_uri,
            "code_verifier": code_verifier,
            "code":          auth_code,
        }

        self.dto = dto
