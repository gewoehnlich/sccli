from typing import Any

from textual import events
from textual.reactive import Reactive, reactive
from textual.widgets import ProgressBar
from loguru import logger

from ui.events.volume_changed import VolumeChanged


class VolumeProgressBar(ProgressBar):
    volume: Reactive[int | None] = reactive(None)

    MAX_VOLUME: int = 100

    def __init__(
        self,
        **kwargs: Any,
    ) -> None:
        super().__init__(
            total=self.MAX_VOLUME,
            show_eta=False,
            show_percentage=False,
            id="volume-progress-bar",
            **kwargs,
        )

    def watch_volume(self, volume: int | None) -> None:
        self.progress = volume or 0

    def on_click(self, event: events.Click) -> None:
        event.stop()

        ratio = event.x / max(self.size.width - 1, 1)
        ratio = min(max(ratio, 0.0), 1.0)

        volume: int = int(ratio * self.MAX_VOLUME)

        self.post_message(
            message=VolumeChanged(
                volume=volume,
            )
        )
