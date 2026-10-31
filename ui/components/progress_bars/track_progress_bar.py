from typing import Any

from textual import events
from textual.reactive import Reactive, reactive
from textual.widgets import ProgressBar

from ui.events.track_current_playtime_changed import TrackCurrentPlaytimeChanged


class TrackProgressBar(ProgressBar):
    current_track_playtime: Reactive[int] = reactive(0)
    current_track_duration: Reactive[int] = reactive(0)

    def __init__(
        self,
        **kwargs: Any,
    ) -> None:
        super().__init__(
            total=None,
            show_eta=False,
            show_percentage=False,
            id="progress_bar",
            **kwargs,
        )

    def watch_current_track_playtime(self) -> None:
        self.progress = self.current_track_playtime

    def watch_current_track_duration(self) -> None:
        self.total = self.current_track_duration

    def on_click(
        self,
        event: events.Click,
    ) -> None:
        event.stop()

        if self.current_track_duration <= 0 or self.size.width <= 0:
            return

        ratio = event.x / max(self.size.width - 1, 1)
        ratio = min(max(ratio, 0.0), 1.0)

        self.post_message(
            message=TrackCurrentPlaytimeChanged(
                playtime=round(ratio * self.current_track_duration),
            )
        )
