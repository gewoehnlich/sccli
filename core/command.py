from abc import abstractmethod
from collections.abc import Callable


class Command:
    @abstractmethod
    async def run(
        self,
        output: Callable[[str], None] | None = None,
    ) -> None: ...
