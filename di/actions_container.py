from core.auth import Auth
from default_settings.messages import MessagesSettings

from actions.fetch_my_liked_tracks_action import FetchMyLikedTracksAction
from actions.get_exit_message_action import GetExitMessageAction
from actions.get_help_message_action import GetHelpMessageAction
from actions.get_unknown_command_message_action import GetUnknownCommandMessageAction
from actions.get_welcome_message_action import GetWelcomeMessageAction
from di.repository_container import RepositoryContainer
from di.requests_container import RequestsContainer


class ActionsContainer:
    def __init__(
        self,
        auth: Auth,
        requests: RequestsContainer,
        repositories: RepositoryContainer,
        messages: MessagesSettings,
    ):
        self.get_welcome_message = GetWelcomeMessageAction(
            message=messages.welcome,
        )

        self.get_exit_message = GetExitMessageAction(message=messages.exit)

        self.get_help_message = GetHelpMessageAction(message=messages.help)

        self.get_unknown_message = GetUnknownCommandMessageAction(
            message=messages.unknown
        )

        self.fetch_my_liked_tracks = FetchMyLikedTracksAction(
            auth=auth,
            request=requests.fetch_my_liked_tracks,
            repository=repositories.track,
        )
