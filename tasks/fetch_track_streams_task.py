from typing import Any

from api_requests.fetch_track_streams_request import FetchTrackStreamsRequest
from core.auth import Auth
from core.task import Task


class FetchTrackStreamsTask(Task):
    def __init__(
        self,
        auth: Auth,
        request: type[FetchTrackStreamsRequest],
    ) -> None:
        super().__init__(
            auth=auth,
            request=request,
        )

    def run(
        self,
        track_urn: str = "soundcloud:tracks:1815509691",
    ) -> dict[str, Any]:
        request = self.request(
            access_token=self.auth.get_access_token(),
            track_urn=track_urn,
        )

        response: dict[str, Any] = request.send()

        return response
