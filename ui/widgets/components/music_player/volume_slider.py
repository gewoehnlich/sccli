from textual.app import ComposeResult
from textual.reactive import Reactive, reactive
from textual.widget import Widget

from core.player import Player
from models.setting import Setting
from repositories.setting_repository import SettingRepository
from ui.components.progress_bars.volume_progress_bar import VolumeProgressBar
from ui.components.statics.volume_static import VolumeStatic
from ui.events.volume_changed import VolumeChanged


class VolumeSlider(Widget):
    volume: Reactive[int | None] = reactive(None)

    def __init__(
        self,
        player: Player,
        setting_repository: SettingRepository,
    ) -> None:
        self.player: Player = player
        self.setting_repository: SettingRepository = setting_repository

        super().__init__(id="volume-slider")

    def compose(self) -> ComposeResult:
        yield VolumeProgressBar().data_bind(
            volume=VolumeSlider.volume,
        )

        yield VolumeStatic().data_bind(
            volume=VolumeSlider.volume,
        )

    def on_mount(self) -> None:
        self.styles.layout = "horizontal"

        self.query_one(VolumeProgressBar)

        volume_static = self.query_one(VolumeStatic)
        volume_static.styles.padding = (0, 0, 0, 1)
        volume_static.styles.width = 4

        volume_setting = self.setting_repository.get_one(
            primary_key="volume",
        )

        if volume_setting:
            self.volume = int(volume_setting.value)

    def watch_volume(self, volume: int | None) -> None:
        if volume:
            self.setting_repository.store(
                model=Setting(
                    name="volume",
                    value=str(volume),
                )
            )

        self.player.update_volume(volume or 0)

    def on_volume_changed(self, event: VolumeChanged) -> None:
        self.volume = event.volume
