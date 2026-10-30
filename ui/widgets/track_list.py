from typing import Any

from textual import events
from textual.reactive import Reactive, reactive
from textual.widgets import DataTable

from core.logger import Logger
from repositories.user_repository import UserRepository
from ui.events.track_selected import TrackSelected
from values.playlist import Playlist


class TrackList(DataTable[None]):
    g_pressed_before: bool = False
    number: int | None = None

    playlist: Reactive[Playlist] = reactive(Playlist(tracks=()))

    def __init__(
        self,
        logger: Logger,
        user_repository: UserRepository,
        track_selected_event: type[TrackSelected],
    ) -> None:
        self.logger: Logger = logger
        self.user_repository: UserRepository = user_repository

        self.track_selected_event: type[TrackSelected] = track_selected_event

        super().__init__()

    def on_mount(self) -> None:
        self.cursor_type = "row"
        self.zebra_stripes = True

    def watch_playlist(self) -> None:
        self.columns = {}
        self.rows = {}

        self.add_columns(*tuple(["id", "username", "title", "duration"]))
        self.add_rows(self.formatted_tracks())

    def formatted_tracks(self) -> list[tuple[Any]]:
        tracks: list[tuple[Any]] = []

        for track in self.playlist.tracks:
            tracks.append(
                tuple([
                    track.id,
                    track.user.username,
                    track.title,
                    track.formatted_duration,
                ])
            )

        return tracks

    def on_key(
        self,
        event: events.Key,
    ) -> None:
        if event.key != "g":
            self.g_pressed_before = False

        if not event.key.isnumeric():
            if event.key != "G":
                self.number = None
        else:
            if self.number is None:
                self.number = 0

            self.number *= 10
            self.number += int(event.key)
            self.number = max(self.number, 0)
            self.number = min(self.number, self.row_count - 1)

        match event.key:
            case "h":
                self.move_cursor(column=self.cursor_column - 1)
            case "j":
                self.move_cursor(row=self.cursor_row + 1)
            case "k":
                self.move_cursor(row=self.cursor_row - 1)
            case "l":
                self.move_cursor(column=self.cursor_column + 1)
            case "g":
                if not self.g_pressed_before:
                    self.g_pressed_before = True

                    return None

                self.move_cursor(row=0)

            case "G":
                self.move_cursor(
                    row=self.number
                    if self.number is not None
                    else self.row_count - 1
                )
            case "H":
                self.move_cursor(column=0)
            case "L":
                self.move_cursor(column=len(self.columns) - 1)

            case _:
                return None

    def on_data_table_row_selected(
        self,
        event: DataTable.RowSelected,
    ) -> None:
        self.post_message(
            message=self.track_selected_event(
                index=event.cursor_row,
            ),
        )
