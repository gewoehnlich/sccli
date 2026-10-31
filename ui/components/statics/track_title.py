from typing import Any

from textual.reactive import Reactive, reactive
from textual.widgets import Static


class TrackTitle(Static):
    title: Reactive[str] = reactive('')

    def __init__(
        self,
        **kwargs: Any,
    ) -> None:
        super().__init__(
            content='',
            id="track_title",
            **kwargs,
        )

    def on_mount(self) -> None:
        self.styles.width = "auto"
        self.styles.margin = (0, 0, 0, 1)

    def watch_title(self) -> None:
        self.content = self.title
