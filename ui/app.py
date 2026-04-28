from typing import Any
from textual.app import App as BaseApp, ComposeResult
from textual.widgets import Footer, Header

from core.logger import Logger
from ui.widgets.music_player import MusicPlayer
from ui.widgets.track_list import TrackList
from repositories.track_repository import TrackRepository


class App(BaseApp):
    TITLE = 'sccli'

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
        yield Header(
            show_clock=True,
            name="sccli",
            id="header"
        )
        yield MusicPlayer()
        yield TrackList(
            track_repository=self.track_repository,
            logger=self.logger,
        )
        yield Footer(
            name="sccli",
            id="footer"
        )

    def on_mount(self) -> None:
        self.theme = "rose-pine"
