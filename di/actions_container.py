from dependency_injector import containers, providers

from actions.fetch_image_action import FetchImageAction
from actions.play_track_action import PlayTrackAction
from actions.sync_my_liked_tracks_action import SyncMyLikedTracksAction
from core.auth import Auth
from core.http_client import HttpClient
from core.logger import Logger
from core.player import Player


class ActionsContainer(containers.DeclarativeContainer):
    auth = providers.Dependency(instance_of=Auth)
    http_client = providers.Dependency(instance_of=HttpClient)
    repositories = providers.DependenciesContainer()
    player = providers.Dependency(instance_of=Player)
    logger = providers.Dependency(instance_of=Logger)

    play_track: providers.Singleton[PlayTrackAction] = providers.Singleton(
        PlayTrackAction,
        auth=auth,
        http_client=http_client,
        player=player,
        track_repository=repositories.track,
        logger=logger,
    )

    fetch_image: providers.Singleton[FetchImageAction] = providers.Singleton(
        FetchImageAction,
        auth=auth,
        http_client=http_client,
        image_repository=repositories.image,
    )

    sync_my_liked_tracks: providers.Singleton[SyncMyLikedTracksAction] = providers.Singleton(
        SyncMyLikedTracksAction,
        auth=auth,
        http_client=http_client,
        user_repository=repositories.user,
        track_repository=repositories.track,
    )
