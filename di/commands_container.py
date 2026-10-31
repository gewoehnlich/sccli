from commands.fetch_my_liked_tracks_command import FetchMyLikedTracksCommand
from commands.output_message_command import OutputMessageCommand
from commands.play_track_command import PlayTrackCommand
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

        self.fetch_my_liked_tracks: FetchMyLikedTracksCommand = (
            FetchMyLikedTracksCommand(
                auth=auth,
                track_repository=repositories.track,
                user_repository=repositories.user,
                http_client=http_client,
            )
        )

        self.play_track: PlayTrackCommand = PlayTrackCommand(
            auth=auth,
            player=player,
            fetch_track_streams_action=actions.fetch_track_streams,
        )
