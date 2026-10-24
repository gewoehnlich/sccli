from typing import Any

from core.action import Action
from core.auth import Auth
from core.player import Player
from core.task import Task
from models.track import Track


class PlayTrackAction(Action):
    def __init__(
        self,
        auth: Auth,
        player: Player,
        fetch_track_streams_task: Task,
    ) -> None:
        self.auth: Auth = auth
        self.player: Player = player
        self.fetch_track_streams_task = fetch_track_streams_task

    def run(
        self,
        track: Track,
    ) -> Any:
        streams: dict[str, Any] = self.fetch_track_streams_task.run(
            track_urn=track.urn,
        )

        streaming_url: str = streams["http_mp3_128_url"]

        self.player.play(
            link=streaming_url,
        )

        return streaming_url
