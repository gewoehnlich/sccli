from textual.reactive import Reactive, reactive
from textual.widgets import Static


class VolumeStatic(Static):
    volume: Reactive[int | None] = reactive(None)

    def on_mount(self) -> None:
        self.styles.width = "auto"
        self.styles.height = "auto"

    def watch_volume(self, volume: int) -> None:
        self.update(content=str(volume or 0))
