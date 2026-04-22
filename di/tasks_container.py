from core.auth import Auth
from core.task import Task
from default_settings.messages import MessagesSettings
from di.repository_container import RepositoryContainer
from di.requests_container import RequestsContainer
from tasks.fetch_track_streaming_url_task import FetchTrackStreamingUrlTask
from tasks.fetch_track_streams_task import FetchTrackStreamsTask


class TasksContainer:
    def __init__(
        self,
        auth: Auth,
        requests: RequestsContainer,
        repositories: RepositoryContainer,
        messages: MessagesSettings,
    ) -> None:
        self.fetch_track_streams: Task = FetchTrackStreamsTask(
            auth=auth,
            request=requests.fetch_track_streams,
        )

        self.fetch_track_streaming_url: Task = FetchTrackStreamingUrlTask(
            auth=auth,
            request=requests.fetch_track_streaming_url,
        )
