from core.auth import Auth
from core.server import Server
from core.task import Task
from default_settings.messages import MessagesSettings
from di.repositories_container import RepositoriesContainer
from di.requests_container import RequestsContainer
from tasks.fetch_track_streams_task import FetchTrackStreamsTask
from tasks.serve_track_task import ServeTrackTask


class TasksContainer:
    def __init__(
        self,
        auth: Auth,
        requests: RequestsContainer,
        repositories: RepositoriesContainer,
        messages: MessagesSettings,
        server: Server,
    ) -> None:
        self.fetch_track_streams: Task = FetchTrackStreamsTask(
            auth=auth,
            request=requests.fetch_track_streams,
        )

        self.serve_track: Task = ServeTrackTask(
            auth=auth,
            request=requests.fetch_track_from_streaming_url,
            server=server,
        )
