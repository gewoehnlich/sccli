from typing import Any
from ui.components.buttons.music_player_button import MusicPlayerButton
from ui.events.next_track_button_pressed import NextTrackButtonPressed


class NextTrackButton(MusicPlayerButton):
    def __init__(
        self,
        **kwargs: Any,
    ) -> None:
        super().__init__(**kwargs)

        self.label = ">|"

    def on_button_pressed(self) -> None:
        self.post_message(NextTrackButtonPressed())
