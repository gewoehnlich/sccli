from dependency_injector import containers, providers
from actions.fetch_my_liked_tracks_action import FetchMyLikedTracksAction
# from actions.get_exit_message_action import GetExitMessageAction
# from actions.get_help_message_action import GetHelpMessageAction
# from actions.get_unknown_command_message_action import GetUnknownCommandMessageAction
from actions.get_welcome_message_action import GetWelcomeMessageAction


class ActionsContainer(containers.DeclarativeContainer):
    # fetch_followings = providers.Singleton(FetchFollowingsAction)
    # fetch_my_liked_tracks       = providers.Singleton(FetchMyLikedTracksAction)
    # get_exit_message            = providers.Singleton(GetExitMessageAction)
    # get_help_message            = providers.Singleton(GetHelpMessageAction)
    # get_unknown_command_message = providers.Singleton(GetUnknownCommandMessageAction)
    get_welcome_message         = providers.Singleton(GetWelcomeMessageAction)

    _instance = None

    def __new__(cls) -> None:
        if cls._instance is None:
            cls._instance = super().__new__(cls)

        return cls._instance
