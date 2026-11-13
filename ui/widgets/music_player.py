from dependency_injector.wiring import Provide, inject
from textual.app import ComposeResult
from textual.containers import Center, Container, Horizontal
from textual.reactive import Reactive, reactive
from textual.widget import Widget

from core.di_container import ActionsContainer, DiContainer
from core.player import Player
from di.commands_container import CommandsContainer
from models.track import Track
from ui.events.current_track_changed import CurrentTrackChanged
from ui.events.track_current_playtime_changed import TrackCurrentPlaytimeChanged
from ui.widgets.components.music_player.buttons import (
    MusicPlayerButtonsComponent,
)
from ui.widgets.components.music_player.image import Image
from ui.widgets.components.music_player.track_metadata import TrackMetadata
from ui.widgets.components.music_player.track_progress_bar import (
    TrackProgressBarComponent,
)
from ui.widgets.components.music_player.volume_slider import VolumeSlider
from values.playlist import Playlist


class MusicPlayer(Widget):
    playlist: Reactive[Playlist] = reactive(Playlist(tracks=()))
    current_track: Reactive[Track | None] = reactive(None)

    is_playing: Reactive[bool] = reactive(False)

    current_track_playtime: Reactive[int] = reactive(0)
    current_track_duration: Reactive[int] = reactive(0)

    @inject
    def __init__(
        self,
        player: Player = Provide[DiContainer.player],
        commands: CommandsContainer = Provide[DiContainer.commands],
        actions: ActionsContainer = Provide[DiContainer.actions],
    ) -> None:
        self.player: Player = player
        self.commands: CommandsContainer = commands
        self.actions: ActionsContainer = actions

        super().__init__()

    def compose(self) -> ComposeResult:
        with Container(id="music-player-container"):
            with Center():
                yield Image()

            with Center():
                yield MusicPlayerButtonsComponent().data_bind(
                    is_playing=MusicPlayer.is_playing,
                )

            with Center():
                yield TrackMetadata().data_bind(
                    current_track=MusicPlayer.current_track,
                )

            with Center():
                yield TrackProgressBarComponent().data_bind(
                    current_track_playtime=MusicPlayer.current_track_playtime,
                    current_track_duration=MusicPlayer.current_track_duration,
                )

            with Horizontal(id="music-player-footer"):
                with Container(id="volume"):
                    yield VolumeSlider()

    def on_mount(self) -> None:
        self.styles.align_horizontal = "center"

        container = self.query_one("#music-player-container")

        for child in container.children:
            child.styles.padding = (0, 0, 1, 0)

        container.styles.align_vertical = "middle"

        image = self.query_one(Image)
        image.styles.width = 50
        image.styles.height = 23
        image.styles.align_horizontal = "center"

        buttons = self.query_one(MusicPlayerButtonsComponent)
        buttons.styles.width = "auto"
        buttons.styles.align_horizontal = "center"

        self.query_one(TrackMetadata)

        progress_bar = self.query_one(TrackProgressBarComponent)
        progress_bar.styles.width = "auto"
        progress_bar.styles.align_horizontal = "center"

        footer = self.query_one("#music-player-footer")
        footer.styles.dock = "bottom"
        footer.styles.width = "100%"
        footer.styles.height = "auto"

        volume = self.query_one("#volume")
        volume.styles.height = "auto"
        volume.styles.align_horizontal = "right"

        volume_slider = self.query_one(VolumeSlider)
        volume_slider.styles.width = "auto"
        volume_slider.styles.height = "auto"

        self.set_interval(1, self.update_current_track_info)

        self.register_player_events()

    def update_current_track_info(self) -> None:
        self.current_track_playtime = self.player.get_current_track_playtime()
        self.current_track_duration = self.player.get_current_track_duration()

    async def play(self, track: Track) -> None:
        self.post_message(
            message=CurrentTrackChanged(
                track=track,
            )
        )

        self.current_track = track
        self.is_playing = True
        await self.actions.play_track().run(track=track)

    async def on_previous_track_button_pressed(self) -> None:
        await self.play(track=self.playlist.prev())

    async def on_play_button_pressed(self) -> None:
        track = self.playlist.current()

        if not track:
            return

        await self.play(track=track)

    def on_pause_button_pressed(self) -> None:
        self.is_playing = False

        self.player.stop()

    async def on_next_track_button_pressed(self) -> None:
        await self.play_next_track()

    def register_player_events(self) -> None:
        self.player.on_track_finished(
            self._on_track_finished,
        )

    def _on_track_finished(self) -> None:
        # runs on mpv's thread, so hand over to the UI thread
        self.app.call_from_thread(self.play_next_track)

    async def play_next_track(self) -> None:
        await self.play(track=self.playlist.next())

    def on_track_current_playtime_changed(
        self, message: TrackCurrentPlaytimeChanged
    ) -> None:
        message.stop()

        if self.playlist.current() is None:
            return

        self.player.update_current_track_playtime(
            playtime=message.playtime,
        )

    async def watch_current_track(self, track: Track | None) -> None:
        image = self.query_one(Image)

        if track is None:
            image.show_default()
            return

        await image.load_artwork(track.artwork_url_large)
