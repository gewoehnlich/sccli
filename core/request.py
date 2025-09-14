import requests

class Request(requests.Request):
    def __init__(self, access_token: str | None = None) -> None:
        self.method:  str = str()
        self.url:     str = str()
        self.headers: dict[str, str] = {
            "Accept": "application/json; charset=utf-8",
            "Content-Type": "application/x-www-form-urlencoded",
        }

        if access_token:
            self.headers['Authorization'] = f"OAuth {access_token}"

        self.params: dict[str, str] = dict()
        self.data:   dict[str, str] = dict()

    def send(self) -> requests.Response:
        response: requests.Response = requests.request(
            method  = self.method,
            url     = self.url,
            headers = self.headers,
            params  = self.params,
            data    = self.data,
            timeout = 30,
        )

        return response
