from core.action import Action


class GetUnknownCommandMessageAction(Action):
    message: str

    def __init__(
        self,
        message: str,
    ):
        self.message = message

    def run(
        self,
    ) -> str:
        return self.message
