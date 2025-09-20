from typing import Any
from requests import request

from core.request import Request
from core.response import Response


class AuthRequest(
    Request
):
    def send(
        self,
    ) -> dict[str, Any]:
        response: Response = request(
            method  = self.method,
            url     = self.url,
            headers = self.headers,
            params  = self.params,
            data    = self.data,
            timeout = 30,
        )

        data: dict[str, Any] = response.json()

        return data
