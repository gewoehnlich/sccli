from typing import Any

from core.action import Action
from core.auth import Auth
from core.http_client import HttpClient
from core.request import Request


class FetchTrackStreamsAction(Action):
    def __init__(
        self,
        auth: Auth,
        http_client: HttpClient,
    ) -> None:
        self.auth: Auth = auth
        self.http_client: HttpClient = http_client

    def run(
        self,
        track_urn: str,
    ) -> dict[str, Any]:
        request: Request = Request(
            method=Request.METHOD.GET,
            url=Request.URL.API + f"/tracks/{track_urn}/streams",
            access_token=self.auth.get_access_token(),
        )

        response: dict[str, Any] = self.http_client.send(request)

        return response
