from typing import Any
from vlc import MediaPlayer
from core.action import Action
from core.auth import Auth
from core.task import Task


class PlayTrackAction(Action):
    def __init__(
        self,
        auth: Auth,
        fetch_track_streams_task: Task,
        fetch_track_streaming_url_task: Task,
    ) -> None:
        super().__init__(
            auth=auth,
        )

        self.fetch_track_streams_task = fetch_track_streams_task
        self.fetch_track_streaming_url_task = fetch_track_streaming_url_task

    def run(
        self,
        track_urn: str = "soundcloud:tracks:1815509691",
    ) -> Any:
        streams: dict[str, Any] = self.fetch_track_streams_task.run(
            track_urn=track_urn,
        )

        streaming_url: str = self.fetch_track_streaming_url_task.run(
            stream_url=streams["http_mp3_128_url"],
        )

        print(streaming_url)

        player = MediaPlayer(streaming_url)
        player.play()
        player.get_instance()

        return streaming_url
