from core.request import Request


class SoundcloudRequest(Request):
    SOUNDCLOUD_API_LINK: str = "https://api.soundcloud.com"

    def __init__(
        self,
        access_token: str,
    ) -> None:
        super().__init__()

        if access_token:
            self.headers["Authorization"] = f"OAuth {access_token}"
