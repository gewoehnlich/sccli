from typing import Any
import subprocess
from core.action import Action
from core.auth import Auth
from core.task import Task
from rich import inspect


class PlayTrackAction(Action):
    def __init__(
        self,
        auth: Auth,
        fetch_track_streams_task: Task,
        serve_track_task: Task,
    ) -> None:
        super().__init__(
            auth=auth,
        )

        self.fetch_track_streams_task = fetch_track_streams_task
        self.serve_track_task = serve_track_task

    def run(
        self,
        track_urn: str = "soundcloud:tracks:2306603633",
    ) -> Any:
        streams: dict[str, Any] = self.fetch_track_streams_task.run(
            track_urn=track_urn,
        )

        streaming_url: str = streams["http_mp3_128_url"]

        # response = self.serve_track_task.run(
        #     streaming_url=streaming_url,
        # )

        # player = MediaPlayer(streaming_url)
        # player.play()
        # player.get_instance()

        subprocess.Popen([
            "mpv",
            f"--http-header-fields=Authorization: Bearer {self.auth.get_access_token()}",
            streaming_url
        ])

        return streaming_url
