from typing import Any
from textual import events
from textual.reactive import Reactive, reactive
from textual.widgets import DataTable

from core.logger import Logger


class TrackList(DataTable):
    g_pressed_before: bool = False
    number: int | None = None
    selected_track: int
    track_columns: list[str]
    tracks: Reactive[list[tuple[Any]]] = reactive([])

    def __init__(
        self,
        track_columns: list[str],
        logger: Logger,
    ) -> None:
        self.track_columns = track_columns
        self.logger = logger

        super().__init__()

    def on_mount(self) -> None:
        self.cursor_type = "row"
        self.zebra_stripes = True

    def watch_tracks(self) -> None:
        self.columns = {}
        self.rows = {}

        self.add_columns(*tuple(self.track_columns))
        self.add_rows(self.tracks)

    def on_key(
        self,
        event: events.Key,
    ) -> None:
        # self.logger.debug(f"Key pressed: {event.key}")
        # self.logger.debug(f"Key pressed: {event.character}")

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
                self.selected_track = self.cursor_row

            case _:
                return None
