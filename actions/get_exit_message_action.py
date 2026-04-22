from core.action import Action


class GetExitMessageAction(Action):
    def __init__(
        self,
        message: str,
    ) -> None:
        self.message = message

    def run(
        self,
    ) -> str:
        return self.message
