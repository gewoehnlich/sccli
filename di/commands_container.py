from dependency_injector import containers, providers

from commands.output_message_command import OutputMessageCommand
from commands.remove_liked_track_command import RemoveLikedTrackCommand
from commands.sync_my_liked_tracks_command import SyncMyLikedTracksCommand
from config.messages import MessagesConfig
from core.auth import Auth
from core.command import Command
from core.http_client import HttpClient
from core.player import Player


class CommandsContainer(containers.DeclarativeContainer):
    auth = providers.Dependency(instance_of=Auth)
    http_client = providers.Dependency(instance_of=HttpClient)
    player = providers.Dependency(instance_of=Player)
    messages = providers.Dependency(instance_of=MessagesConfig)
    actions = providers.DependenciesContainer()
    repositories = providers.DependenciesContainer()

    welcome: providers.Singleton[Command] = providers.Singleton(
        OutputMessageCommand,
        message=messages.provided.welcome,
    )

    exit: providers.Singleton[Command] = providers.Singleton(
        OutputMessageCommand,
        message=messages.provided.exit,
    )

    help: providers.Singleton[Command] = providers.Singleton(
        OutputMessageCommand,
        message=messages.provided.help,
    )

    unknown: providers.Singleton[Command] = providers.Singleton(
        OutputMessageCommand,
        message=messages.provided.unknown,
    )

    sync_my_liked_tracks: providers.Singleton[SyncMyLikedTracksCommand] = (
        providers.Singleton(
            SyncMyLikedTracksCommand,
            auth=auth,
            track_repository=repositories.track,
            user_repository=repositories.user,
            image_repository=repositories.image,
            http_client=http_client,
        )
    )

    remove_liked_track: providers.Singleton[RemoveLikedTrackCommand] = (
        providers.Singleton(
            RemoveLikedTrackCommand,
            auth=auth,
            http_client=http_client,
            track_repository=repositories.track,
        )
    )
