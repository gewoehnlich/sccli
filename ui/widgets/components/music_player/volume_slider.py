from textual import events
from textual.app import ComposeResult
from textual.reactive import Reactive, reactive
from textual.widget import Widget
from textual.widgets import ProgressBar, Static
from loguru import logger

from core.player import Player
from ui.components.progress_bars.volume_progress_bar import VolumeProgressBar
from ui.components.statics.volume_static import VolumeStatic
from ui.events.volume_changed import VolumeChanged


class VolumeSlider(Widget):
    volume: Reactive[int] = reactive(0)

    def __init__(
        self,
        player: Player,
    ) -> None:
        self.player: Player = player

        super().__init__(
            id="volume-slider"
        )

    def compose(self) -> ComposeResult:
        yield VolumeProgressBar().data_bind(
            volume=VolumeSlider.volume,
        )

        yield VolumeStatic().data_bind(
            volume=VolumeSlider.volume,
        )

    def on_mount(self) -> None:
        self.styles.width = "100%"
        self.styles.height = "auto"
        self.styles.layout = "horizontal"
        self.styles.align_horizontal = "center"
        self.styles.text_align = "center"

        volume_static = self.query_one(VolumeStatic)
        volume_static.styles.padding = (0, 0, 0, 1)

    def watch_volume(self, volume: int) -> None:
        self.player.update_volume(volume)

    def on_volume_changed(self, event: VolumeChanged) -> None:
        self.volume = event.volume
