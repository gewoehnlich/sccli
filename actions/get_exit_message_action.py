from dependency_injector.wiring import Provide
from core.action import Action
from core.di_container import DiContainer


class GetExitMessageAction(Action):
    def run(
        config: str = Provide[DiContainer.config]
    ) -> str:
        return config.exit_command_message
