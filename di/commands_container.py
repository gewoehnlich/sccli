from dependency_injector import containers, providers

from commands.exit_command import ExitCommand
from commands.my_liked_tracks_command import MyLikedTracksCommand
from commands.followings_command import FollowingsCommand
from commands.followings_tracks_command import FollowingsTracksCommand
from commands.track_command import TrackCommand
from commands.track_streaming_url_command import TrackStreamingUrlCommand
from commands.help_command import HelpCommand
from commands.my_tracks_command import MyTracksCommand
from commands.unknown_command import UnknownCommand
from commands.user_command import UserCommand
from commands.welcome_command import WelcomeCommand


class CommandsContainer(containers.DeclarativeContainer):
    requests  = providers.DependenciesContainer()
    actions   = providers.DependenciesContainer()
    resources = providers.DependenciesContainer()

    # exit                = providers.Singleton(ExitCommand)
    # my_liked_tracks     = providers.Singleton(MyLikedTracksCommand)
    # followings          = providers.Singleton(FollowingsCommand)
    # followings_tracks   = providers.Singleton(FollowingsTracksCommand)
    # track               = providers.Singleton(TrackCommand)
    # track_streaming_url = providers.Singleton(TrackStreamingUrlCommand)
    # help                = providers.Singleton(HelpCommand)
    # my_tracks           = providers.Singleton(MyTracksCommand)
    # unknown_command     = providers.Singleton(UnknownCommand)
    # user                = providers.Singleton(UserCommand)
    welcome             = providers.Singleton(
        WelcomeCommand,
        actions.get_welcome_message,
        resources.pprint,
    )
