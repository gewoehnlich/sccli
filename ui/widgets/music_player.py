from textual.app import ComposeResult
from textual.containers import Vertical
from textual.reactive import Reactive, reactive
from textual.widget import Widget
from models.track import Track
from ui.widgets.components.music_player.buttons import MusicPlayerButtonsComponent
from ui.widgets.components.music_player.image import Image
from ui.widgets.components.music_player.track_progress_bar import TrackProgressBarComponent
from values.selected_track_index import SelectedTrackIndex


class MusicPlayer(Widget):
    tracks: Reactive[list[Track]] = reactive([])
    selected_track_index: Reactive[SelectedTrackIndex] = reactive(SelectedTrackIndex())

    is_playing: Reactive[bool] = reactive(False)

    current_track_playtime: Reactive[int] = reactive(0)
    current_track_duration: Reactive[int] = reactive(0)

    def compose(self) -> ComposeResult:
        self.image = Image()
        yield self.image

        self.buttons = MusicPlayerButtonsComponent()
        yield self.buttons.data_bind(
            is_playing=MusicPlayer.is_playing,
        )

        self.progress_bar = TrackProgressBarComponent()
        yield self.progress_bar.data_bind(
            current_track_playtime=MusicPlayer.current_track_playtime,
            current_track_duration=MusicPlayer.current_track_duration,
        )

    def on_mount(self) -> None:
        self.styles.layout = "vertical"

        self.image.styles.width = 30
        self.image.styles.height = 15

        self.set_interval(1, self.update_current_track_info)

        self.register_player_events()

    def update_current_track_info(self) -> None:
        self.current_track_playtime = self.app.player.get_current_track_playtime()
        self.current_track_duration = self.app.player.get_current_track_duration()

    def on_previous_track_button_pressed(self) -> None:
        self.is_playing = True

        self.app.di_container.actions.play_track.run(
            track=self.tracks[self.selected_track_index.previous(
                tracks=self.tracks,
            )]
        )

    def on_play_button_pressed(self) -> None:
        self.is_playing = True

        self.app.di_container.actions.play_track.run(
            track=self.tracks[self.selected_track_index.value()]
        )

    def on_pause_button_pressed(self) -> None:
        self.is_playing = False

        self.app.player.stop()

    def on_next_track_button_pressed(self) -> None:
        self.is_playing = True

        self.app.di_container.actions.play_track.run(
            track=self.tracks[self.selected_track_index.next(
                tracks=self.tracks,
            )]
        )

    def register_player_events(self) -> None:
        self.app.player.on_track_finished(
            self.play_next_track,
        )

    def play_next_track(self) -> None:
        self.app.di_container.actions.play_track.run(
            track=self.tracks[self.selected_track_index.next(
                tracks=self.tracks,
            )]
        )
