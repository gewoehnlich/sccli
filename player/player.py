from typing import Any
import rich
from textual.app import App, ComposeResult
from textual.widgets import DataTable

from repositories.track_repository import TrackRepository


class Player(App):
    def __init__(
        self,
        track_repository: TrackRepository,
        **kwargs: Any,
    ) -> None:
        super().__init__(**kwargs)

        self.track_repository = track_repository

    def compose(self) -> ComposeResult:
        yield DataTable()

    def on_mount(self) -> None:
        table = self.query_one(DataTable)

        table.add_columns(*self.track_repository.model.columns())
        table.add_rows([track.to_tuple() for track in self.track_repository.get()[:100]])
