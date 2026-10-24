from config.messages import MessagesConfig
from core.auth import Auth
from core.task import Task
from di.repositories_container import RepositoriesContainer
from tasks.fetch_track_streams_task import FetchTrackStreamsTask


class TasksContainer:
    def __init__(
        self,
        auth: Auth,
        repositories: RepositoriesContainer,
        messages: MessagesConfig,
    ) -> None:
        self.fetch_track_streams: Task = FetchTrackStreamsTask(
            auth=auth,
        )
