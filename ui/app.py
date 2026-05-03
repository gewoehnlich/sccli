from typing import Any
from textual.app import App as BaseApp, ComposeResult
from textual.reactive import Reactive, reactive
from textual.widgets import Footer, Header

from core.logger import Logger
from ui.widgets.music_player import MusicPlayer
from ui.widgets.shell import Shell
from ui.widgets.track_list import TrackList
from repositories.track_repository import TrackRepository
from views.track_view import TrackView


class App(BaseApp):
    TITLE = 'sccli'

    tracks: Reactive[list[tuple[Any]]] = reactive([])
    selected_track_urn: Reactive[str | None] = reactive(None)

    def __init__(
        self,
        track_repository: TrackRepository,
        logger: Logger,
        track_view: TrackView,
        **kwargs: Any,
    ) -> None:
        super().__init__(**kwargs)

        self.track_repository = track_repository
        self.logger = logger
        self.track_view = track_view

    def compose(self) -> ComposeResult:
        yield Header(
            show_clock=True,
            name="sccli",
            id="header"
        )
        yield MusicPlayer()
        yield TrackList(
            track_columns=self.track_view.fields,
            logger=self.logger,
        )
        yield Shell()
        yield Footer(
            name="sccli",
            id="footer"
        )

    def on_mount(self) -> None:
        self.theme = "rose-pine"
        self.styles.height = "auto"

        self.tracks = [
            self.track_view.to_tuple(track) for track in self.track_repository.get()[:41]
        ]
        self.logger.info(self.tracks)

    def watch_tracks(self) -> None:
        self.query_one(TrackList).tracks = self.tracks
