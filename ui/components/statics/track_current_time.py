import math
from typing import Any
from textual.reactive import Reactive, reactive
from textual.widgets import Static


class TrackCurrentTime(Static):
    seconds: Reactive[int] = reactive(0)

    def __init__(
        self,
        **kwargs: Any,
    ) -> None:
        super().__init__(
            content="0:00",
            id="track_current_time",
            **kwargs,
        )

    def on_mount(self) -> None:
        self.styles.width = "auto"
        self.styles.margin = (0, 1, 0, 0)

    def watch_seconds(self) -> None:
        self.content = self.formatted_seconds()

    def formatted_seconds(self) -> str:
        seconds = math.ceil(self.seconds)

        minutes: int = math.floor(seconds / 60)
        seconds %= 60

        return f"{minutes}:{seconds:02d}"
