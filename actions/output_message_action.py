from dataclasses import dataclass

from core.action import Action
from core.types import ShellOutputMethod


@dataclass(slots=True, kw_only=True, frozen=True)
class OutputMessageAction(Action):
    message: str

    async def run(
        self,
        output: ShellOutputMethod | None = None,
    ) -> None:
        if output:
            output(self.message)
