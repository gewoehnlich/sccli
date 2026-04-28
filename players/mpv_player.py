import subprocess
from core.auth import Auth
from core.player import Player


class MpvPlayer(Player):
    def __init__(
        self,
        player: str,
        auth: Auth,
    ) -> None:
        self.auth: Auth = auth

        self.__player = subprocess.Popen([
            "mpv"
        ])

    def track(
        self,
        link: str,
    ) -> None:
        pass

    def play(self) -> None:
        self.__player
