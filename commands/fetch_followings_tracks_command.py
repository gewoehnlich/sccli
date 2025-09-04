from core.action import Action
from core.command import Command
from core.resource import Resource


class FetchFollowingsTracksCommand(Command):
    _instance = None

    def __new__(cls) -> None:
        if cls._instance is None:
            cls._instance = super().__new__(cls)

        return cls._instance

    def __init__(
        action: Action,
        resource: Resource,
    ) -> None:
        super().__init__(
            action = action,
            resource = resource,
        )
