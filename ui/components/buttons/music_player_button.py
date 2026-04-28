from typing import Any
from textual.widgets import Button


class MusicPlayerButton(Button):
    def __init__(
        self,
        **kwargs: Any,
    ) -> None:
        super().__init__(**kwargs)

        self.styles.width = "5%"
