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
