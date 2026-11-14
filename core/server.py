from abc import ABC, abstractmethod
from dataclasses import dataclass

from values.callback_result import CallbackResult


@dataclass(slots=True, kw_only=True, frozen=True)
class Server(ABC):
    host: str
    port: int
    path: str

    @abstractmethod
    def start(self) -> None:
        """Bind and listen. Must be called before the browser is opened."""

    @abstractmethod
    def wait_for_callback(self, timeout: float) -> CallbackResult: ...

    @abstractmethod
    def stop(self) -> None: ...
