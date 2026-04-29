from typing import Any
from textual.widgets import Static


class TrackTotalTime(Static):
    def __init__(
        self,
        **kwargs: Any,
    ) -> None:
        super().__init__(
            content="0:00",
            id="track_total_time",
            **kwargs,
        )

    def on_mount(self) -> None:
        self.styles.width = "auto"
        self.styles.margin = (0, 0, 0, 1)
