from typing import Any
from ui.components.buttons.music_player_button import MusicPlayerButton
from ui.events.pause_button_pressed import PauseButtonPressed


class PauseButton(MusicPlayerButton):
    def __init__(
        self,
        **kwargs: Any,
    ) -> None:
        super().__init__(**kwargs)

        self.label = "||"

    def on_button_pressed(self) -> None:
        self.post_message(PauseButtonPressed())
