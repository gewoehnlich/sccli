from abc import ABC, abstractmethod

from values.callback_result import CallbackResult


class Server(ABC):
    def __init__(
        self,
        port: int,
        path: str,
    ) -> None:
        self.port = port
        self.path = path

    @abstractmethod
    def start(self) -> None:
        """Bind and listen. Must be called before the browser is opened."""

    @abstractmethod
    def wait_for_callback(self, timeout: float) -> CallbackResult: ...

    @abstractmethod
    def stop(self) -> None: ...
