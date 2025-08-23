from src.core.request import Request

class RefreshTokenRequest(Request):
    def __init__(
        self,
        client_id: str,
        client_secret: str,
        refresh_token: str,
    ) -> None:
        super().__init__()

        self.method = "POST"

        self.url = "https://secure.soundcloud.com/oauth/token"

        self.data = {
            "grant_type":    "refresh_token",
            "client_id":     client_id,
            "client_secret": client_secret,
            "refresh_token": refresh_token,
        }
