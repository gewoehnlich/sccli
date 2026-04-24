from typing import Any

from core.auth import Auth
from core.request import Request
from core.server import Server
from core.task import Task


class ServeTrackTask(Task):
    def __init__(
        self,
        auth: Auth,
        request: type[Request],
        server: Server,
    ) -> None:
        super().__init__(
            auth=auth,
            request=request,
        )

        self.server = server

    def run(
        self,
        streaming_url: str,
    ) -> dict[str, Any]:
        request = self.request(
            access_token=self.auth.get_access_token(),
            url=streaming_url,
        )

        response: dict[str, Any] = request.send()

        return response
