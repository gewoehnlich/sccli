from commands.exit_command                import ExitCommand
from commands.my_liked_tracks_command     import MyLikedTracksCommand
from commands.followings_command          import FollowingsCommand
from commands.followings_tracks_command   import FollowingsTracksCommand
from commands.track_command               import TrackCommand
from commands.track_streaming_url_command import TrackStreamingUrlCommand
from commands.help_command                import HelpCommand
from commands.my_tracks_command           import MyTracksCommand
from commands.unknown_command             import UnknownCommand
from commands.user_command                import UserCommand
from commands.welcome_command             import WelcomeCommand
from di.actions_container import ActionsContainer
from di.resources_container import ResourcesContainer


class CommandsContainer(

):
    def __init__(
        self,
        actions: ActionsContainer,
        resources: ResourcesContainer,
    ):
        self.welcome = WelcomeCommand(
            action = actions.get_welcome_message,
            resource = resources.pprint,
        )

        self.exit = ExitCommand(
            action = actions.get_exit_message,
            resource = resources.pprint,
        )

        self.help = HelpCommand(
            action = actions.get_help_message,
            resource = resources.pprint,
        )

        self.unknown = UnknownCommand(
            action = actions.get_unknown_message,
            resource = resources.pprint,
        )

        self.liked_tracks = MyLikedTracksCommand(
            action = actions.fetch_my_liked_tracks,
            resource = resources.pprint,
        )
