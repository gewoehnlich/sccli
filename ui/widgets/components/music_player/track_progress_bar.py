from textual.app import ComposeResult
from textual.reactive import Reactive, reactive
from textual.widget import Widget

from ui.components.progress_bars.track_progress_bar import TrackProgressBar
from ui.components.statics.track_current_time import TrackCurrentTime
from ui.components.statics.track_total_time import TrackTotalTime


class TrackProgressBarComponent(Widget):
    current_track_playtime: Reactive[int] = reactive(0)
    current_track_duration: Reactive[int] = reactive(0)

    def compose(self) -> ComposeResult:
        yield TrackCurrentTime().data_bind(
            seconds=TrackProgressBarComponent.current_track_playtime,
        )
        yield TrackProgressBar()
        yield TrackTotalTime().data_bind(
            seconds=TrackProgressBarComponent.current_track_duration,
        )

    def on_mount(self) -> None:
        self.styles.layout = "horizontal"
        self.styles.dock = "bottom"
        self.styles.width = "auto"
        self.styles.height = "auto"
