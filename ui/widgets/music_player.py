from textual.app import ComposeResult
from textual.reactive import Reactive, reactive
from textual.widget import Widget
from models.track import Track
from ui.widgets.components.music_player.buttons import MusicPlayerButtonsComponent
from ui.widgets.components.music_player.track_progress_bar import TrackProgressBarComponent


class MusicPlayer(Widget):
    selected_track: Reactive[Track | None] = reactive(None)

    def compose(self) -> ComposeResult:
        yield MusicPlayerButtonsComponent()
        yield TrackProgressBarComponent()

    def on_mount(self) -> None:
        self.styles.height = "100%"
        self.styles.width = "50%"

    def on_play_button_pressed(self) -> None:
        self.app.logger.info("play button pressed")
        self.app.di_container.actions.play_track.run(self.selected_track)

    def on_pause_button_pressed(self) -> None:
        self.app.logger.info("pause button pressed")
        self.app.player.stop()
