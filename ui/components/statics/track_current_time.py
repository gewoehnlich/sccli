from typing import Any
from textual.widgets import Static


class TrackCurrentTime(Static):
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
