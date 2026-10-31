from typing import Any

from textual.reactive import Reactive, reactive
from textual.widgets import Static


class TrackUsername(Static):
    username: Reactive[str] = reactive('')

    def __init__(
        self,
        **kwargs: Any,
    ) -> None:
        super().__init__(
            content='',
            id="track_username",
            **kwargs,
        )

    def on_mount(self) -> None:
        self.styles.width = "auto"
        self.styles.margin = (0, 0, 0, 1)

    def watch_username(self) -> None:
        self.content = self.username
