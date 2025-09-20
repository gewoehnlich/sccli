from requests import request

from core.dto import Dto
from core.request import Request
from core.response import Response


class SoundcloudRequest(
    Request
):
    SOUNDCLOUD_API_LINK: str = 'https://api.soundcloud.com'

    dto: Dto | None = None


    def __init__(
        self,
        access_token: str | None = None,
        dto: Dto | None = None,
    ) -> None:
        if access_token:
            self.headers['Authorization'] = f"OAuth {access_token}"

        if dto:
            self.dto = dto


    def send(
        self,
    ) -> Dto:
        response: Response = request(
            method  = self.method,
            url     = self.url,
            headers = self.headers,
            params  = self.params,
            data    = self.data,
            timeout = 30,
        )

        data: dict[str, Any] = response.json()

        self.dto = self.dto.from_dict(
            data = data,
        )

        return self.dto
