from textual.app import App as BaseApp, ComposeResult
from textual.containers import Horizontal, Vertical
from textual.reactive import Reactive, reactive
from textual.widgets import Footer, Header

from core.di_container import DiContainer
from core.logger import Logger
from core.player import Player
from di.actions_container import ActionsContainer
from di.commands_container import CommandsContainer
from models.track import Track
from repositories.setting_repository import SettingRepository
from repositories.track_repository import TrackRepository
from ui.events.track_selected import TrackSelected
from ui.widgets.music_player import MusicPlayer
from ui.widgets.shell import Shell
from ui.widgets.track_list import TrackList
from values.playlist import Playlist


class App(BaseApp[None]):
    TITLE = "sccli"

    playlist: Reactive[Playlist] = reactive(Playlist(tracks=()))
    current_track: Reactive[Track | None] = reactive(None)

    def __init__(
        self,
        di_container: DiContainer,
    ) -> None:
        self.di_container = di_container

        self.track_repository: TrackRepository = di_container.repositories.track
        self.logger: Logger = di_container.logger
        self.commands: CommandsContainer = di_container.commands
        self.player: Player = di_container.player
        self.actions: ActionsContainer = di_container.actions
        self.setting_repository: SettingRepository = (
            di_container.repositories.setting
        )

        super().__init__()

    def compose(self) -> ComposeResult:
        yield Header(
            show_clock=True,
            id="header",
        )

        with Horizontal(id="main"):
            with Vertical(id="left"):
                yield MusicPlayer(
                    player=self.player,
                    commands=self.commands,
                    actions=self.actions,
                    setting_repository=self.setting_repository,
                ).data_bind(
                    playlist=App.playlist,
                    current_track=App.current_track,
                )
                yield Shell(
                    id="shell",
                    commands=self.commands,
                )

            yield TrackList(
                logger=self.logger,
                user_repository=self.di_container.repositories.user,
            ).data_bind(
                playlist=App.playlist,
            )

        yield Footer(id="footer")

    def on_mount(self) -> None:
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

        track_list = self.query_one(TrackList)
        track_list.styles.max_width = "100%"
        track_list.styles.height = "100%"

        self.playlist = Playlist(
            tracks=self.track_repository.get(),
        )

        if len(self.playlist) > 0:
            self.current_track = self.playlist.random()

    def on_track_selected(self, event: TrackSelected) -> None:
        event.stop()
        track = self.playlist.select(index=event.index)
        self.query_one(MusicPlayer).play(track)
