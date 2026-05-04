from abc import abstractmethod


class Player:
    def __init__(
        self,
    ) -> None:
        pass

    @abstractmethod
    def play(self, filename: str) -> None:
        pass

    @abstractmethod
    def stop(self) -> None:
        pass

    @abstractmethod
    def next(self) -> None:
        pass

    @abstractmethod
    def prev(self) -> None:
        pass
