from typing import Any

from core.auth import Auth
from core.request import Request
from core.task import Task


class FetchTrackStreamsTask(Task):
    def __init__(
        self,
        auth: Auth,
    ) -> None:
        self.auth: Auth = auth

    def run(
        self,
        track_urn: str = "soundcloud:tracks:1815509691",
    ) -> dict[str, Any]:
        request: Request = Request(
            method=Request.METHOD.GET,
            url=Request.URL.API + f"/tracks/{track_urn}/streams",
            access_token=self.auth.access_token(),
        )

        response: dict[str, Any] = request.send()

        return response
