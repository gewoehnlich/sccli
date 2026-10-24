from abc import abstractmethod
from typing import Any


class Task:
    @abstractmethod
    def run(
        self,
    ) -> Any:
        pass
