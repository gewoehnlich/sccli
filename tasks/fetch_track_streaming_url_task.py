from typing import Any
from api_requests.fetch_track_streaming_url_request import FetchTrackStreamingUrlRequest
from core.auth import Auth
from core.task import Task

class FetchTrackStreamingUrlTask(Task):
    def __init__(
        self,
        auth: Auth,
        request: type[FetchTrackStreamingUrlRequest],
    ) -> None:
        super().__init__(
            auth=auth,
            request=request,
        )

    def run(
        self,
        stream_url: str,
    ) -> dict[str, Any]:
        print({'stream_url': stream_url})
        request = self.request(
            access_token=self.auth.get_access_token(),
            url=stream_url,
        )

        print(request)

        response: dict[str, Any] = request.send()
        print(response)

        return response
