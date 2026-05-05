from typing import Any
from textual import events
from textual.reactive import Reactive, reactive
from textual.widgets import DataTable

from core.logger import Logger
from models.track import Track
from ui.events.track_selected import TrackSelected
from views.track_view import TrackView


class TrackList(DataTable):
    g_pressed_before: bool = False
    number: int | None = None

    tracks: Reactive[list[tuple[Any]]] = reactive([])
    selected_track: Reactive[Track | None] = reactive(None)

    def __init__(
        self,
        track_view: TrackView,
        logger: Logger,
        track_selected_event: type[TrackSelected],
    ) -> None:
        self.track_view = track_view
        self.logger = logger

        self.track_selected_event = track_selected_event

        super().__init__()

    def on_mount(self) -> None:
        self.cursor_type = "row"
        self.zebra_stripes = True

        self.styles.width = "50%"
        self.styles.height = "100%"

    def watch_tracks(self) -> None:
        self.columns = {}
        self.rows = {}

        self.add_columns(*tuple(self.track_view.fields))
        self.add_rows(self.formatted_tracks())

    def formatted_tracks(self) -> list[tuple[Any]]:
        return [
            self.track_view.to_tuple(track) for track in self.tracks
        ]

    def watch_selected_track(self) -> None:
        self.post_message(
            message=self.track_selected_event(
                track=self.selected_track,
            ),
        )

    def on_key(
        self,
        event: events.Key,
    ) -> None:
        if event.key != 'g':
            self.g_pressed_before = False

        if not event.key.isnumeric():
            if event.key != 'G':
                self.number = None
        else:
            if self.number is None:
                self.number = 0

            self.number *= 10
            self.number += int(event.key)
            self.number = max(self.number, 0)
            self.number = min(self.number, self.row_count - 1)

        match event.key:
            case 'h':
                self.move_cursor(
                    column = self.cursor_column - 1
                )
            case 'j':
                self.move_cursor(
                    row = self.cursor_row + 1
                )
            case 'k':
                self.move_cursor(
                    row = self.cursor_row - 1
                )
            case 'l':
                self.move_cursor(
                    column = self.cursor_column + 1
                )
            case 'g':
                if not self.g_pressed_before:
                    self.g_pressed_before = True

                    return None

                self.move_cursor(
                    row = 0
                )

            case 'G':
                self.move_cursor(
                    row = self.number if self.number is not None else self.row_count - 1
                )
            case 'H':
                self.move_cursor(
                    column = 0
                )
            case 'L':
                self.move_cursor(
                    column = len(self.columns) - 1
                )
            case 'enter':
                # self.logger.info(self.tracks)
                # self.logger.info(self.cursor_row)
                self.selected_track = self.tracks[self.cursor_row]

            case _:
                return None
