from typing import Self
from dependency_injector.wiring import Provide, inject

from core.action import Action
from core.command import Command
from core.resource import Resource


class WelcomeCommand(Command):
    _instance:    Self | None = None
    _initialized: bool        = False

    def __new__(
        cls: type[Self],
        *args,
        **kwargs,
    ) -> Self:
        if cls._instance is None:
            cls._instance = super().__new__(cls)

        return cls._instance

    @inject
    def __init__(
        self,
        action: Action = Provide["DiContainer.actions.welcome_action"],
        resource: Resource = Provide["DiContainer.resources.pprint"],
    ) -> None:
        super().__init__(
            action = action,
            resource = resource,
        )
