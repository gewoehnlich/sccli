from textual.app import ComposeResult
from textual.reactive import Reactive, reactive
from textual.widget import Widget

from ui.components.buttons.next_track_button import NextTrackButton
from ui.components.buttons.pause_button import PauseButton
from ui.components.buttons.play_button import PlayButton
from ui.components.buttons.previous_track_button import PreviousTrackButton


class MusicPlayerButtonsComponent(Widget):
    is_playing: Reactive[bool] = reactive(False)

    def compose(self) -> ComposeResult:
        yield PreviousTrackButton()
        yield PlayButton()
        yield PauseButton()
        yield NextTrackButton()

    def on_mount(self) -> None:
        self.styles.layout = "horizontal"
        self.styles.width = "100%"

    def watch_is_playing(self) -> None:
        if self.is_playing is True:
            self.query_one(PlayButton).display = "none"
            self.query_one(PauseButton).display = "block"
        else:
            self.query_one(PlayButton).display = "block"
            self.query_one(PauseButton).display = "none"
