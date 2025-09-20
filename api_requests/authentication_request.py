from core.request import Request

class AuthenticationRequest(Request):
    def __init__(
        self,
        client_id:     str | None = None,
        client_secret: str | None = None,
        redirect_uri:  str | None = None,
        code_verifier: str | None = None,
        auth_code:     str | None = None,
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
