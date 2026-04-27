from textual.app import ComposeResult
from textual.widget import Widget
from textual.widgets import Button


class MusicPlayer(Widget):
    def compose(self) -> ComposeResult:
        yield Button()
        yield Button()
        yield Button()
