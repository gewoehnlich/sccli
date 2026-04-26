from typing import Any
from textual.app import App, ComposeResult

from core.logger import Logger
from player.widgets.track_list import TrackList
from repositories.track_repository import TrackRepository


class Player(App):
    def __init__(
        self,
        track_repository: TrackRepository,
        logger: Logger,
        **kwargs: Any,
    ) -> None:
        super().__init__(**kwargs)

        self.track_repository = track_repository
        self.logger = logger

    def compose(self) -> ComposeResult:
        yield TrackList(
            track_repository=self.track_repository,
            logger=self.logger,
        )

    def on_mount(self) -> None:
        pass
