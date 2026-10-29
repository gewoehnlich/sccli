from abc import abstractmethod
from collections.abc import Callable


class Player:
    def __init__(
        self,
    ) -> None:
        self._track_finished_callbacks: list[Callable[[], None]] = []

    def on_track_finished(
        self,
        callback: Callable[[], None],
    ) -> None:
        self._track_finished_callbacks.append(callback)

    def emit_track_finished(
        self,
    ) -> None:
        for callback in self._track_finished_callbacks:
            callback()

    @abstractmethod
    def play(self, link: str) -> None:
        pass

    @abstractmethod
    def stop(self) -> None:
        pass

    @abstractmethod
    def get_current_track_playtime(self) -> int:
        pass

    @abstractmethod
    def get_current_track_duration(self) -> int:
        pass
