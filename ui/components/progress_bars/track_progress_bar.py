from typing import Any
from textual.widgets import ProgressBar


class TrackProgressBar(ProgressBar):
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
