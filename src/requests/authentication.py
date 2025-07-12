from src.core.request import Request
import requests

class AuthenticationRequest(Request):
    def __init__(
        self,
        client_id: str,
        client_secret: str,
        redirect_uri: str,
        code_verifier: str,
        auth_code: str,
    ) -> None:
        super().__init__()

        self.url = "https://secure.soundcloud.com/oauth/token"
        self.data = {
            "grant_type":    "authorization_code",
            "client_id":     client_id,
            "client_secret": client_secret,
            "redirect_uri":  redirect_uri,
            "code_verifier": code_verifier,
            "code":          auth_code
        }


    def send(self) -> requests.Response:
        response = requests.post(
            url     = self.url, 
            headers = self.headers, 
            data    = self.data
        )

        return response
