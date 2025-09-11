from typing import Self
from core.action import Action
from core.command import Command
from core.resource import Resource


class FollowingsTracksCommand(Command):
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

    def __init__(
        self,
        action: Action,
        resource: Resource,
    ) -> None:
        super().__init__(
            action = action,
            resource = resource,
        )
