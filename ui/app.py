from typing import Any
from textual.app import App as BaseApp, ComposeResult
from textual.containers import Horizontal
from textual.message import Message
from textual.reactive import Reactive, reactive
from textual.widgets import Footer, Header

from core.di_container import DiContainer
from core.logger import Logger
from core.player import Player
from di.commands_container import CommandsContainer
from models.track import Track
from repositories.track_repository import TrackRepository
from ui.events.track_selected import TrackSelected
from ui.widgets.music_player import MusicPlayer
from ui.widgets.shell import Shell
from ui.widgets.track_list import TrackList
from views.track_view import TrackView


class App(BaseApp):
    TITLE = 'sccli'

    tracks: Reactive[list[Track]] = reactive([])
    selected_track: Reactive[Track | None] = reactive(None)

    track_selected_event: type[Message] = TrackSelected

    def __init__(
        self,
        di_container: DiContainer,
    ) -> None:
        self.di_container = di_container

        self.track_repository: TrackRepository = di_container.repositories.track
        self.track_view: TrackView = di_container.views.track
        self.logger: Logger = di_container.logger
        self.commands: CommandsContainer = di_container.commands
        self.player: Player = di_container.player

        super().__init__()

    def compose(self) -> ComposeResult:
        yield Header(
            show_clock=True,
            id="header",
        )
        with Horizontal():
            yield MusicPlayer()
            yield TrackList(
                track_view=self.track_view,
                logger=self.logger,

                track_selected_event=self.track_selected_event,
            )
        yield Shell()
        yield Footer(
            id="footer"
        )

    def on_mount(self) -> None:
        self.theme = "rose-pine"
        self.styles.height = "auto"

        self.tracks = self.track_repository.get()

    def watch_tracks(self) -> None:
        self.query_one(TrackList).tracks = self.tracks

    def watch_selected_track(self) -> None:
        self.query_one(MusicPlayer).selected_track = self.selected_track

    def on_track_selected(
        self,
        message: TrackSelected,
    ) -> None:
        self.selected_track = message.track
