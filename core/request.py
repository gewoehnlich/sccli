from typing import Any
import requests

from core.dto import Dto
from core.response import Response


class Request(
    requests.Request
):
    method:  str = str()
    url:     str = str()
    headers: dict[str, str] = {
        "Accept": "application/json; charset=utf-8",
        "Content-Type": "application/x-www-form-urlencoded",
    }
    params: dict[str, str] = {}
    data:   dict[str, str] = {}

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
        response: Response = requests.request(
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
