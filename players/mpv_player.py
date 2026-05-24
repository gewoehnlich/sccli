import mpv
import rich
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

        self.auth: Auth = auth
        self.logger = logger
        self.player = mpv.MPV(
            log_handler=self.__log, ytdl=True,
            http_header_fields=f"Authorization: Bearer { self.auth.get_access_token() }",
            http_proxy=http_proxy,
        )

        @self.player.event_callback("end-file")
        def on_end_file(event: mpv.MpvEventEndFile) -> None:
            event = event.as_dict()

            if event["reason"] == b'eof':
                self.logger.info('track finished')

                self.emit_track_finished()

        self.logger.info(self.player._event_callbacks)

    def __log(
        self,
        level: str,
        prefix: str,
        text: str,
    ) -> None:
        self.logger.debug(f"[{level}] {prefix}: {text}")

    def play(
        self,
        link: str,
    ) -> None:
        if self.player.pause == True:
            self.player.pause = False
        else:
            self.player.play(
                filename=link,
            )

    def stop(
        self,
    ) -> None:
        self.player.pause = True

    def get_current_track_playtime(self) -> int:
        return self.player.time_pos or 0

    def get_current_track_duration(self) -> int:
        return self.player.duration or 0
