from typing import Any
from ui.components.buttons.music_player_button import MusicPlayerButton


class NextTrackButton(MusicPlayerButton):
    def __init__(
        self,
        **kwargs: Any,
    ) -> None:
        super().__init__(**kwargs)

        self.label = ">|"
