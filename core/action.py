from abc import abstractmethod
from typing import Any


class Action:
    @abstractmethod
    def run(
        self,
    ) -> Any:
        pass
