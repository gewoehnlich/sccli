from textual.reactive import Reactive, reactive
from textual.widgets import Static


class TrackTitle(Static):
    title: Reactive[str] = reactive("")

    def on_mount(self) -> None:
        self.styles.width = "100%"
        self.styles.height = "auto"

    def watch_title(self) -> None:
        self.update(self.title)
