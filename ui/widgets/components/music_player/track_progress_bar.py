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
        self.track_playtime = TrackCurrentTime()
        yield self.track_playtime.data_bind(
            seconds=TrackProgressBarComponent.current_track_playtime,
        )

        self.progress_bar = TrackProgressBar()
        yield self.progress_bar.data_bind(
            current_track_playtime=TrackProgressBarComponent.current_track_playtime,
            current_track_duration=TrackProgressBarComponent.current_track_duration,
        )

        self.track_duration = TrackTotalTime()
        yield self.track_duration.data_bind(
            seconds=TrackProgressBarComponent.current_track_duration,
        )

    def on_mount(self) -> None:
        self.styles.layout = "horizontal"
        self.styles.width = "100%"
        self.styles.height = "auto"

        self.track_playtime.styles.width = "auto"
        self.track_playtime.styles.margin = (0, 1, 0, 0)

        self.progress_bar.styles.width = "auto"

        self.track_duration.styles.width = "auto"
        self.track_duration.styles.margin = (0, 0, 0, 1)
