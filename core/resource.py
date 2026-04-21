from abc import abstractmethod
from typing import Any


class Resource:
    @abstractmethod
    def print(
        self,
        data: Any,
    ) -> None:
        pass
