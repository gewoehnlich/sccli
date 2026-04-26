from typing import Any
from textual.widgets import DataTable

from repositories.track_repository import TrackRepository


class TrackList(DataTable):
    def __init__(
        self,
        track_repository: TrackRepository,
        **kwargs: Any,
    ) -> None:
        super().__init__(**kwargs)

        self.track_repository = track_repository

    def on_mount(self) -> None:
        self.add_columns(*self.track_repository.model.columns())
        self.add_rows([track.to_tuple() for track in self.track_repository.get()[:100]])
