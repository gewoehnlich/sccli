from typing import Any

from core.command import Command
from core.types import ShellOutputMethod


class OutputMessageCommand(Command):
    def __init__(self, message: str) -> None:
        self.message: str = message

    async def run(
        self,
        output: ShellOutputMethod | None = None,
        **kwargs: dict[str, Any],
    ) -> None:
        if output:
            output(self.message)
