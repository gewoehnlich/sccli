from collections.abc import Callable
from typing import Any

from core.auth import Auth
from core.command import Command
from core.player import Player
from core.task import Task
from models.track import Track
from tasks.fetch_track_streams_task import FetchTrackStreamsTask


class PlayTrackCommand(Command):
    def __init__(
        self,
        auth: Auth,
        player: Player,
        fetch_track_streams_task: Task,
    ) -> None:
        self.auth: Auth = auth
        self.player: Player = player
        self.fetch_track_streams_task: FetchTrackStreamsTask = fetch_track_streams_task

    def run(
        self,
        track: Track,
        output: Callable[[str], None] | None = None,
    ) -> Any:
        streams: dict[str, Any] = self.fetch_track_streams_task.run(
            track_urn=track.urn,
        )

        streaming_url: str = streams["hls_aac_160_url"]

        self.player.play(
            link=streaming_url,
        )

        return streaming_url
