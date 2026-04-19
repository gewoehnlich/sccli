from core.action import Action


class GetWelcomeMessageAction(
    Action
):
    message: str

    def __init__(
        self,
        message: str,
    ) -> None:
        self.message = message

    def run(
        self,
    ) -> str:
        return self.message
