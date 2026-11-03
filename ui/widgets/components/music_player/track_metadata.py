from textual.app import ComposeResult
from textual.reactive import Reactive, reactive
from textual.widget import Widget

from models.track import Track
from ui.components.statics.track_title import TrackTitle
from ui.components.statics.track_username import TrackUsername


class TrackMetadata(Widget):
    current_track: Reactive[Track | None] = reactive(None)

    username: Reactive[str] = reactive("")
    title: Reactive[str] = reactive("")

    def compose(self) -> ComposeResult:
        yield TrackUsername().data_bind(
            username=TrackMetadata.username,
        )

        yield TrackTitle().data_bind(
            title=TrackMetadata.title,
        )

    def on_mount(self) -> None:
        self.styles.width = "100%"
        self.styles.height = "auto"

        username = self.query_one(TrackUsername)
        username.styles.width = "100%"
        username.styles.margin = (0, 0, 0, 1)
        username.styles.text_align = "center"

        title = self.query_one(TrackTitle)
        title.styles.width = "100%"
        title.styles.margin = (0, 0, 0, 1)
        title.styles.text_align = "center"

    def watch_current_track(self, track: Track | None) -> None:
        if track is None:
            self.username = ""
            self.title = ""

            return

        self.username = track.user.username
        self.title = track.title
