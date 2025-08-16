class Request:
    def __init__(self, access_token: str | None = None) -> None:
        self.url: str = ""
        self.headers: dict[str, str] = {
            "Accept": "application/json; charset=utf-8",
            "Content-Type": "application/x-www-form-urlencoded",
        }

        if access_token:
            self.headers['Authorization'] = f"OAuth {access_token}"

        self.data: dict[str, str] = {}
