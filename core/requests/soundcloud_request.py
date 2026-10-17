from core.request import Request
from domain.enums.soundcloud_api_endpoint_enum import SoundcloudApiEndpointEnum


class SoundcloudRequest(Request):
    SOUNDCLOUD_API_LINK: str = SoundcloudApiEndpointEnum.API.value

    def __init__(
        self,
        access_token: str,
        method: str,
        url: str,
        headers: dict[str, str] | None = None,
        params: dict[str, str] | None = None,
        data: dict[str, str] | None = None,
    ) -> None:
        if data is None:
            data = {}
        if params is None:
            params = {}
        if headers is None:
            headers = {}
        if access_token:
            headers["Authorization"] = f"OAuth {access_token}"

        super().__init__(
            method=method,
            url=url,
            headers=headers,
            params=params,
            data=data,
        )
