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
        self.auth: Auth = auth
        self.logger = logger
        self.player = mpv.MPV(
            log_handler=self.__log,
            ytdl=True,
            http_header_fields=f"Authorization: Bearer { self.auth.get_access_token() }",
            http_proxy=http_proxy,
        )

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
