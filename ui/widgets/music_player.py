from textual.app import ComposeResult
from textual.containers import Center
from textual.reactive import Reactive, reactive
from textual.widget import Widget

from core.player import Player
from di.commands_container import CommandsContainer
from ui.events.track_current_playtime_changed import TrackCurrentPlaytimeChanged
from ui.widgets.components.music_player.buttons import (
    MusicPlayerButtonsComponent,
)
from ui.widgets.components.music_player.image import Image
from ui.widgets.components.music_player.track_progress_bar import (
    TrackProgressBarComponent,
)
from values.playlist import Playlist


class MusicPlayer(Widget):
    playlist: Reactive[Playlist] = reactive(Playlist(tracks=()))

    is_playing: Reactive[bool] = reactive(False)

    current_track_playtime: Reactive[int] = reactive(0)
    current_track_duration: Reactive[int] = reactive(0)

    def __init__(
        self,
        player: Player,
        commands: CommandsContainer,
    ) -> None:
        self.player: Player = player
        self.commands: CommandsContainer = commands

        super().__init__()

    def compose(self) -> ComposeResult:
        with Center():
            yield Image()

        with Center():
            yield MusicPlayerButtonsComponent().data_bind(
                is_playing=MusicPlayer.is_playing,
            )

        with Center():
            yield TrackProgressBarComponent().data_bind(
                current_track_playtime=MusicPlayer.current_track_playtime,
                current_track_duration=MusicPlayer.current_track_duration,
            )

    def on_mount(self) -> None:
        self.styles.width = "auto"
        self.styles.height = "auto"
        self.styles.align_horizontal = "center"

        image = self.query_one(Image)
        image.styles.width = 30
        image.styles.height = 15
        image.styles.align_horizontal = "center"

        buttons = self.query_one(MusicPlayerButtonsComponent)
        buttons.styles.width = "auto"
        buttons.styles.align_horizontal = "center"
        buttons.styles.padding = 1

        progress_bar = self.query_one(TrackProgressBarComponent)
        progress_bar.styles.width = "auto"
        progress_bar.styles.align_horizontal = "center"

        self.set_interval(1, self.update_current_track_info)

        self.register_player_events()

    def update_current_track_info(self) -> None:
        self.current_track_playtime = self.player.get_current_track_playtime()
        self.current_track_duration = self.player.get_current_track_duration()

    def on_previous_track_button_pressed(self) -> None:
        self.is_playing = True

        self.commands.play_track.run(
            track=self.playlist.prev(),
        )

    def on_play_button_pressed(self) -> None:
        track = self.playlist.current()

        if not track:
            return

        self.is_playing = True

        self.commands.play_track.run(
            track=track,
        )

    def on_pause_button_pressed(self) -> None:
        self.is_playing = False

        self.player.stop()

    def on_next_track_button_pressed(self) -> None:
        self.is_playing = True

        self.commands.play_track.run(
            track=self.playlist.next(),
        )

    def register_player_events(self) -> None:
        self.player.on_track_finished(
            self.play_next_track,
        )

    def play_next_track(self) -> None:
        self.commands.play_track.run(
            track=self.playlist.next(),
        )

    def on_track_current_playtime_changed(
        self,
        message: TrackCurrentPlaytimeChanged,
    ) -> None:
        message.stop()

        if self.playlist.current() is None:
            return

        self.player.update_current_track_playtime(
            playtime=message.playtime,
        )
