from dependency_injector.wiring import Provide
from core.action import Action


class GetWelcomeMessageAction(Action):
    def run(
        config
    ) -> str:
        return config.welcome_command_message
