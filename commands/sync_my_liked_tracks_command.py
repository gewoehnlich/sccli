from actions.sync_my_liked_tracks_action import SyncMyLikedTracksAction
from core.command import Command
from core.types import ShellOutputMethod


class SyncMyLikedTracksCommand(Command):
    def __init__(self, action: SyncMyLikedTracksAction) -> None:
        self.action: SyncMyLikedTracksAction = action

    async def run(self, output: ShellOutputMethod | None = None) -> None:
        await self.action.run(output=output)
