from typing import Any

from core.auth import Auth
from core.http_client import HttpClient
from core.request import Request
from core.task import Task


class FetchTrackStreamsTask(Task):
    def __init__(
        self,
        auth: Auth,
        http_client: HttpClient,
    ) -> None:
        self.auth: Auth = auth
        self.http_client: HttpClient = http_client

    def run(
        self,
        track_urn: str = "soundcloud:tracks:1815509691",
    ) -> dict[str, Any]:
        request: Request = Request(
            method=Request.METHOD.GET,
            url=Request.URL.API + f"/tracks/{track_urn}/streams",
            access_token=self.auth.access_token(),
        )

        response: dict[str, Any] = self.http_client.send(request)

        return response
