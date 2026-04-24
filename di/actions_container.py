from actions.fetch_my_liked_tracks_action import FetchMyLikedTracksAction
from actions.get_exit_message_action import GetExitMessageAction
from actions.get_help_message_action import GetHelpMessageAction
from actions.get_unknown_command_message_action import GetUnknownCommandMessageAction
from actions.get_welcome_message_action import GetWelcomeMessageAction
from actions.play_track_action import PlayTrackAction
from core.action import Action
from core.auth import Auth
from default_settings.messages import MessagesSettings
from di.repository_container import RepositoryContainer
from di.requests_container import RequestsContainer
from di.tasks_container import TasksContainer


class ActionsContainer:
    def __init__(
        self,
        auth: Auth,
        requests: RequestsContainer,
        repositories: RepositoryContainer,
        messages: MessagesSettings,
        tasks: TasksContainer,
    ) -> None:
        self.get_welcome_message: Action = GetWelcomeMessageAction(
            message=messages.welcome,
        )

        self.get_exit_message: Action = GetExitMessageAction(
            message=messages.exit
        )

        self.get_help_message: Action = GetHelpMessageAction(
            message=messages.help
        )

        self.get_unknown_message: Action = GetUnknownCommandMessageAction(
            message=messages.unknown
        )

        self.fetch_my_liked_tracks: Action = FetchMyLikedTracksAction(
            auth=auth,
            request=requests.fetch_my_liked_tracks,
            repository=repositories.track,
        )

        self.play_track: Action = PlayTrackAction(
            auth=auth,
            fetch_track_streams_task=tasks.fetch_track_streams,
            serve_track_task=tasks.serve_track,
        )
