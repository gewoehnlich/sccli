from typing import Any
from textual.app import App, ComposeResult
from textual.widgets import DataTable

from models.track import Track
from repositories.track_repository import TrackRepository


class Player(App):
    CSS = """
    Screen { align: center middle; }
    Digits { width: auto; }
    """

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

        tracks = self.track_repository.get()
        formatted_tracks = [track.to_tuple() for track in tracks[:100]]

        table.add_columns('id', 'title', 'description', 'urn', 'duration')
        table.add_rows(formatted_tracks)
