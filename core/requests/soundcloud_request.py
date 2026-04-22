from core.request import Request


class SoundcloudRequest(Request):
    SOUNDCLOUD_API_LINK: str = "https://api.soundcloud.com"

    def __init__(
        self,
        access_token: str,
        method: str,
        url: str,
        headers: dict[str, str] = {},
        params: dict[str, str] = {},
        data: dict[str, str] = {},
    ) -> None:
        if access_token:
            headers["Authorization"] = f"OAuth {access_token}"

        super().__init__(
            method=method,
            url=url,
            headers=headers,
            params=params,
            data=data,
        )
