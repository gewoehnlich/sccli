from typing import Any
from textual.app import App, ComposeResult
from textual.widgets import Footer, Header

from core.logger import Logger
from player.widgets.music_player import MusicPlayer
from player.widgets.track_list import TrackList
from repositories.track_repository import TrackRepository


class Player(App):
    TITLE = 'sccli'

    CSS_PATH = "style.tcss"

    def __init__(
        self,
        track_repository: TrackRepository,
        logger: Logger,
        **kwargs: Any,
    ) -> None:
        super().__init__(**kwargs)

        self.track_repository = track_repository
        self.logger = logger

        self.theme = "rose-pine"

    def compose(self) -> ComposeResult:
        yield Header(
            show_clock=True,
            name="sccli",
            id="header"
        )
        # yield MusicPlayer()
        yield TrackList(
            track_repository=self.track_repository,
            logger=self.logger,
        )
        yield Footer(
            name="sccli",
            id="footer"
        )

    def on_mount(self) -> None:
        pass
