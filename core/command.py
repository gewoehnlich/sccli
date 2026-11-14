from abc import abstractmethod
from typing import Any

from core.types import ShellOutputMethod


class Command:
    @abstractmethod
    async def run(
        self,
        output: ShellOutputMethod | None = None,
        **kwargs: dict[str, Any],
    ) -> None: ...
