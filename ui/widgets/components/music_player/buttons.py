from textual.app import ComposeResult
from textual.widget import Widget

from ui.components.buttons.next_track_button import NextTrackButton
from ui.components.buttons.pause_button import PauseButton
from ui.components.buttons.play_button import PlayButton
from ui.components.buttons.previous_track_button import PreviousTrackButton


class MusicPlayerButtonsComponent(Widget):
    def compose(self) -> ComposeResult:
        yield PreviousTrackButton()
        yield PlayButton()
        yield PauseButton()
        yield NextTrackButton()

    def on_mount(self) -> None:
        self.styles.layout = "horizontal"
