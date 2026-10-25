from collections.abc import Callable

from core.command import Command


class OutputMessageCommand(Command):
    def __init__(
        self,
        message: str,
    ) -> None:
        self.message: str = message

    def run(
        self,
        output: Callable[[str], None] | None = None,
    ) -> None:
        if output:
            output(self.message)
