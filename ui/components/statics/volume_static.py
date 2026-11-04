from textual.reactive import Reactive, reactive
from textual.widgets import Static


class VolumeStatic(Static):
    volume: Reactive[int] = reactive(0)

    def on_mount(self) -> None:
        self.styles.width = "100%"
        self.styles.height = "auto"

    def watch_volume(self, volume: int) -> None:
        self.update(content=str(volume))
