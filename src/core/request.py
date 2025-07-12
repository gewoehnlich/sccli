class Request:
    def __init__(self) -> None:
        self.url: str = ""
        self.headers: dict[str, str] = {
            "Accept": "application/json; charset=utf-8",
            "Content-Type": "application/x-www-form-urlencoded"
        }

        self.data: dict[str, str] = {}
