from textual.app import ComposeResult
from textual.widget import Widget

from ui.components.progress_bars.track_progress_bar import TrackProgressBar
from ui.components.statics.track_current_time import TrackCurrentTime
from ui.components.statics.track_total_time import TrackTotalTime


class TrackProgressBarComponent(Widget):
    def compose(self) -> ComposeResult:
        yield TrackCurrentTime()
        yield TrackProgressBar()
        yield TrackTotalTime()

    def on_mount(self) -> None:
        self.styles.layout = "horizontal"
        self.styles.dock = "bottom"
        self.styles.width = "auto"
        self.styles.height = "auto"
