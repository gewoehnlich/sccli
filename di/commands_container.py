from commands.output_message_command import OutputMessageCommand
from commands.play_track_command import PlayTrackCommand
from commands.remove_liked_track_command import RemoveLikedTrackCommand
from commands.sync_my_liked_tracks_command import SyncMyLikedTracksCommand
from config.messages import MessagesConfig
from core.auth import Auth
from core.command import Command
from core.http_client import HttpClient
from core.player import Player
from di.actions_container import ActionsContainer
from di.repositories_container import RepositoriesContainer


class CommandsContainer:
    def __init__(
        self,
        actions: ActionsContainer,
        auth: Auth,
        repositories: RepositoriesContainer,
        messages: MessagesConfig,
        player: Player,
        http_client: HttpClient,
    ) -> None:
        self.welcome: Command = OutputMessageCommand(
            message=messages.welcome,
        )

        self.exit: Command = OutputMessageCommand(
            message=messages.exit,
        )

        self.help: Command = OutputMessageCommand(
            message=messages.help,
        )

        self.unknown: Command = OutputMessageCommand(
            message=messages.unknown,
        )

        self.sync_my_liked_tracks: SyncMyLikedTracksCommand = (
            SyncMyLikedTracksCommand(
                auth=auth,
                track_repository=repositories.track,
                user_repository=repositories.user,
                image_repository=repositories.image,
                http_client=http_client,
            )
        )

        self.play_track: PlayTrackCommand = PlayTrackCommand(
            auth=auth,
            player=player,
            fetch_track_streams_action=actions.fetch_track_streams,
        )

        self.remove_liked_track: RemoveLikedTrackCommand = (
            RemoveLikedTrackCommand(
                auth=auth,
                http_client=http_client,
                track_repository=repositories.track,
            )
        )
