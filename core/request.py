from typing import Any
from aiohttp.web import Response
import requests

from core.dto import Dto


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

    dto: Dto


    def __init__(
        self,
    ) -> None:
        pass


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
