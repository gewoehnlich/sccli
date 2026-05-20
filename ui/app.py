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
from values.selected_track_index import SelectedTrackIndex


class App(BaseApp):
    TITLE = 'sccli'

    tracks: Reactive[list[Track]] = reactive([])
    selected_track_index: Reactive[SelectedTrackIndex] = reactive(SelectedTrackIndex())

    track_selected_event: type[Message] = TrackSelected

    def __init__(
        self,
        di_container: DiContainer,
    ) -> None:
        self.di_container = di_container

        self.track_repository: TrackRepository = di_container.repositories.track
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
            yield MusicPlayer().data_bind(
                selected_track_index=App.selected_track_index,
                tracks=App.tracks,
            )
            yield TrackList(
                track_view=self.di_container.views.track,
                logger=self.logger,

                track_selected_event=self.track_selected_event,
            ).data_bind(
                selected_track_index=App.selected_track_index,
                tracks=App.tracks,
            )
        yield Shell()
        yield Footer(
            id="footer"
        )

    def on_mount(self) -> None:
        self.theme = "rose-pine"
        self.styles.height = "100%"

        self.query_one(MusicPlayer).styles.max_width = "50%"
        self.query_one(MusicPlayer).styles.height = "100%"
        self.query_one(TrackList).styles.max_width = "50%"
        self.query_one(TrackList).styles.height = "100%"

        self.tracks = self.track_repository.get()

    def on_track_selected(
        self,
        message: TrackSelected,
    ) -> None:
        self.selected_track_index.with_value(
            index=message.index,
        )
