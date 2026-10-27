from actions.fetch_track_streams_action import FetchTrackStreamsAction
from core.auth import Auth
from core.http_client import HttpClient


class ActionsContainer:
    def __init__(
        self,
        auth: Auth,
        http_client: HttpClient,
    ) -> None:
        self.fetch_track_streams: FetchTrackStreamsAction = (
            FetchTrackStreamsAction(
                auth=auth,
                http_client=http_client,
            )
        )
