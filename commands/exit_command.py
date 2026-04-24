import sys

from core.command import Command


class ExitCommand(Command):
    def run(
        self,
    ) -> None:
        super().run()

        sys.exit(1)
