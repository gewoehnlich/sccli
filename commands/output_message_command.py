from collections.abc import Callable
from typing import Any

from core.command import Command


class OutputMessageCommand(Command):
    def __init__(self, message: str) -> None:
        self.message: str = message

    async def run(
        self,
        output: Callable[[str], None] | None = None,
        **kwargs: dict[str, Any],
    ) -> None:
        if output:
            output(self.message)
