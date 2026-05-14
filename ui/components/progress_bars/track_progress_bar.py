from typing import Any
from textual.reactive import Reactive, reactive
from textual.widgets import ProgressBar


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
