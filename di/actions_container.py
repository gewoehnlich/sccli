from actions.fetch_image_action import FetchImageAction
from actions.fetch_track_streams_action import FetchTrackStreamsAction
from core.auth import Auth
from core.http_client import HttpClient
from di.repositories_container import RepositoriesContainer
from repositories import image_repository


class ActionsContainer:
    def __init__(
        self,
        auth: Auth,
        http_client: HttpClient,
        repositories: RepositoriesContainer,
    ) -> None:
        self.fetch_track_streams: FetchTrackStreamsAction = (
            FetchTrackStreamsAction(
                auth=auth,
                http_client=http_client,
            )
        )

        self.fetch_image: FetchImageAction = FetchImageAction(
            auth=auth,
            http_client=http_client,
            image_repository=repositories.image,
        )
