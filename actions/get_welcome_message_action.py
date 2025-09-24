from dependency_injector.wiring import Provide
from core.action import Action


class GetWelcomeMessageAction(
    Action
):
    def run(
        self,
        message: str = Provide[DiContainer.actions.get_welcome_command_message],
    ) -> str:
        return message
