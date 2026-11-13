from dependency_injector.wiring import Provide, inject
from textual.app import App as BaseApp, ComposeResult
from textual.containers import Horizontal, Vertical
from textual.reactive import Reactive, reactive
from textual.widgets import Footer, Header

from core.di_container import DiContainer
from core.logger import Logger
from models.track import Track
from repositories.track_repository import TrackRepository
from ui.events.current_track_changed import CurrentTrackChanged
from ui.events.track_selected import TrackSelected
from ui.widgets.music_player import MusicPlayer
from ui.widgets.shell import Shell
from ui.widgets.track_list import TrackList
from values.playlist import Playlist


class App(BaseApp[None]):
    TITLE = "sccli"

    playlist: Reactive[Playlist] = reactive(Playlist(tracks=()))
    current_track: Reactive[Track | None] = reactive(None)

    @inject
    def __init__(
        self,
        logger: Logger = Provide[DiContainer.logger],
        track_repository: TrackRepository = Provide[
            DiContainer.repositories().track
        ],
    ) -> None:
        super().__init__()

        self.logger: Logger = logger
        self.track_repository: TrackRepository = track_repository

    def compose(self) -> ComposeResult:
        yield Header(
            show_clock=True,
            id="header",
        )

        with Horizontal(id="main"):
            with Vertical(id="left"):
                yield MusicPlayer().data_bind(
                    playlist=App.playlist,
                    current_track=App.current_track,
                )
                yield Shell().data_bind(
                    current_track=App.current_track,
                )

            yield TrackList().data_bind(
                playlist=App.playlist,
            )

        yield Footer(id="footer")

    async def on_mount(self) -> None:
        self.theme = "rose-pine"
        self.styles.height = "100%"

        left = self.query_one("#left")
        left.styles.padding = 1

        music_player = self.query_one(MusicPlayer)
        music_player.styles.width = "1fr"
        music_player.styles.height = "1fr"
        music_player.styles.align = ("center", "middle")

        shell = self.query_one(Shell)
        shell.styles.max_width = "100%"
        shell.styles.height = "40%"

        self.logger.attach_sink(shell.write)

        track_list = self.query_one(TrackList)
        track_list.styles.max_width = "100%"
        track_list.styles.height = "100%"

        self.playlist = Playlist(
            tracks=await self.track_repository.get(),
        )

        if len(self.playlist) > 0:
            self.current_track = self.playlist.random()

    async def on_track_selected(self, event: TrackSelected) -> None:
        event.stop()
        track = self.playlist.select(index=event.index)
        await self.query_one(MusicPlayer).play(track)

    async def on_current_track_changed(
        self, event: CurrentTrackChanged
    ) -> None:
        self.current_track = event.track
