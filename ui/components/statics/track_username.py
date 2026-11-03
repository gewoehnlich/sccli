from textual.reactive import Reactive, reactive
from textual.widgets import Static


class TrackUsername(Static):
    username: Reactive[str] = reactive("")

    def on_mount(self) -> None:
        self.styles.width = "100%"
        self.styles.height = "auto"

    def watch_username(self, username: str) -> None:
        self.update(content=username)
