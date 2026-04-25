from abc import abstractmethod


class Server:
    def __init__(
        self,
        port: int,
        path: str,
    ) -> None:
        self.port = port
        self.path = path

    @abstractmethod
    def run(
        self,
    ) -> None:
        ...

    @abstractmethod
    def stop(
        self,
    ) -> None:
        ...
