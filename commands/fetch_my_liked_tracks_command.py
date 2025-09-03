from dependency_injector.wiring import Provide
from core.action import Action
from core.command import Command
from core.di_container import DiContainer

def fetch_my_liked_tracks_command(
    action: Action,
    args: list[str],
) -> None:
    result: bool = action()

    # to-do: handle true / false

class FetchMyLikedTracksCommand(Command):
    _instance = None

    def __new__(cls) -> None:
        if cls._instance is None:
            cls._instance = super().__new__(cls)

        return cls._instance

    def __init__(
        action: Action,
        resource: Resource,
    ) -> None:
        self.action = action
        self.resource = resource
