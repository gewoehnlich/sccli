from textual.app import ComposeResult
from textual.widget import Widget
from ui.widgets.components.music_player.buttons import MusicPlayerButtonsComponent
from ui.widgets.components.music_player.track_progress_bar import TrackProgressBarComponent


class MusicPlayer(Widget):
    def compose(self) -> ComposeResult:
        yield MusicPlayerButtonsComponent()
        yield TrackProgressBarComponent()

    def on_mount(self) -> None:
        self.styles.height = "100%"
        self.styles.width = "50%"
