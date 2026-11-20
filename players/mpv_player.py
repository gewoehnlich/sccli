from collections.abc import Callable
from typing import cast

import mpv

from core.auth import Auth
from core.logger import Logger
from core.player import Player


class MpvPlayer(Player):
    def __init__(
        self,
        auth: Auth,
        http_proxy: str | None,
        logger: Logger,
    ) -> None:
        super().__init__()

        self._auth: Auth = auth
        self._logger: Logger = logger
        self._player: mpv.MPV = mpv.MPV(
            # log_handler=self._log,
            ytdl=True,
            vid="no",
            volume=60,
            http_proxy=http_proxy,
        )
        self._current_streaming_link: str | None = None

        @self._player.event_callback("end-file")
        def on_end_file(event: mpv.MpvEventEndFile) -> None:
            event = event.as_dict()

            if event["reason"] == b"eof":
                self.emit_track_finished()

    def _log(self, level: str, prefix: str, text: str) -> None:
        self._logger.debug(f"[{level}] {prefix}: {text}")

    async def play(self, link: str) -> None:
        if cast(bool, self._player.pause):
            self._player.pause = False

        if self._current_streaming_link != link:
            self._player.http_header_fields = [
                f"Authorization: Bearer {await self._auth.get_access_token()}"
            ]
            self._current_streaming_link = link
            cast(Callable[..., None], self._player.play)(filename=link)

    def stop(self) -> None:
        self._player.pause = True

    def get_current_track_playtime(self) -> int:
        return cast(int, self._player.time_pos) or 0

    def get_current_track_duration(self) -> int:
        return cast(int, self._player.duration) or 0

    def update_current_track_playtime(self, playtime: int) -> None:
        self._player.time_pos = playtime

    def update_volume(self, volume: int) -> None:
        self._player.volume = volume
