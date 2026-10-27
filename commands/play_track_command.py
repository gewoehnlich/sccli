from collections.abc import Callable
from typing import Any, cast

from actions.fetch_track_streams_action import FetchTrackStreamsAction
from core.action import Action
from core.auth import Auth
from core.command import Command
from core.player import Player
from models.track import Track


class PlayTrackCommand(Command):
    def __init__(
        self,
        auth: Auth,
        player: Player,
        fetch_track_streams_action: Action,
    ) -> None:
        self.auth: Auth = auth
        self.player: Player = player
        self.fetch_track_streams_action: FetchTrackStreamsAction = (
            fetch_track_streams_action
        )

    def run(
        self,
        track: Track,
        output: Callable[[str], None] | None = None,
    ) -> Any:
        streams: dict[str, Any] = self.fetch_track_streams_action.run(
            track_urn=track.urn,
        )

        streaming_url: str = cast(
            str,
            streams.get("hls_aac_160_url") or streams.get("hls_mp3_128_url"),
        )

        self.player.play(
            link=streaming_url,
        )

        return streaming_url
