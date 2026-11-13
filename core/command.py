from abc import abstractmethod
from collections.abc import Callable
from typing import Any


class Command:
    @abstractmethod
    async def run(
        self,
        output: Callable[[str], None] | None = None,
        **kwargs: dict[str, Any],
    ) -> None: ...
