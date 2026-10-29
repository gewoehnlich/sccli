from collections.abc import Sequence
from typing import Any

from textual import events
from textual.reactive import Reactive, reactive
from textual.widgets import DataTable

from core.logger import Logger
from models.track import Track
from models.user import User
from repositories.user_repository import UserRepository
from ui.events.track_selected import TrackSelected
from ui.widgets.components.track_list.views.track_view import TrackView
from values.selected_track_index import SelectedTrackIndex


class TrackList(DataTable[None]):
    g_pressed_before: bool = False
    number: int | None = None

    tracks: Reactive[Sequence[Track]] = reactive([])
    selected_track_index: Reactive[SelectedTrackIndex] = reactive(
        SelectedTrackIndex()
    )

    def __init__(
        self,
        track_view: type[TrackView],
        logger: Logger,
        track_selected_event: type[TrackSelected],
        user_repository: UserRepository,
    ) -> None:
        self.track_view: type[TrackView] = track_view
        self.logger: Logger = logger

        self.track_selected_event: type[TrackSelected] = track_selected_event

        self.user_repository: UserRepository = user_repository

        super().__init__()

    def on_mount(self) -> None:
        self.cursor_type = "row"
        self.zebra_stripes = True

    def watch_tracks(self) -> None:
        self.columns = {}
        self.rows = {}

        self.add_columns(*tuple(self.track_view.fields))
        self.add_rows(self.formatted_tracks())

    def formatted_tracks(self) -> list[tuple[Any]]:
        tracks: list[tuple[Any]] = []

        for track in self.tracks:
            user: User | None = self.user_repository.get_one(
                primary_key=track.user_id,
            )

            if not user:
                self.logger.warning(f"user_id {track.user_id} not found in the database")
                continue

            view: TrackView = self.track_view(
                track=track,
                user=user,
            )

            tracks.append(view.view())

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
