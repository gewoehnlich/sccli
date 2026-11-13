from dependency_injector import containers, providers

from actions.fetch_image_action import FetchImageAction
from actions.fetch_track_streams_action import FetchTrackStreamsAction
from core.auth import Auth
from core.http_client import HttpClient
from di.repositories_container import RepositoriesContainer


class ActionsContainer(containers.DeclarativeContainer):
    auth = providers.Dependency(instance_of=Auth)

    http_client = providers.Dependency(instance_of=HttpClient)

    repositories = providers.DependenciesContainer()

    fetch_track_streams: providers.Singleton[FetchTrackStreamsAction] = providers.Singleton(
        FetchTrackStreamsAction,
        auth=auth,
        http_client=http_client,
        track_repository=repositories.track,
    )

    fetch_image: providers.Singleton[FetchImageAction] = providers.Singleton(
        FetchImageAction,
        auth=auth,
        http_client=http_client,
        image_repository=repositories.image,
    )
