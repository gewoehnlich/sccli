from commands.exit_command import ExitCommand
from commands.my_liked_tracks_command import MyLikedTracksCommand
from commands.help_command import HelpCommand
from commands.unknown_command import UnknownCommand
from commands.welcome_command import WelcomeCommand
from di.actions_container import ActionsContainer
from di.resources_container import ResourcesContainer


class CommandsContainer:
    def __init__(
        self,
        actions: ActionsContainer,
        resources: ResourcesContainer,
    ):
        self.welcome = WelcomeCommand(
            action=actions.get_welcome_message,
        )

        self.exit = ExitCommand(
            action=actions.get_exit_message,
        )

        self.help = HelpCommand(
            action=actions.get_help_message,
        )

        self.unknown = UnknownCommand(
            action=actions.get_unknown_message,
        )

        self.liked_tracks = MyLikedTracksCommand(
            action=actions.fetch_my_liked_tracks,
            resource=resources.pprint,
        )
