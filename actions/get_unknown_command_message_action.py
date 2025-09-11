from dependency_injector.wiring import Provide
from core.action import Action
from core.di_container import DiContainer


class GetUnknownCommandMessageAction(Action):
    def run(
        config: str = Provide[DiContainer.config]
    ) -> str:
        return config.unknown_command_message
