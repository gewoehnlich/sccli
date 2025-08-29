from sqlite3 import Cursor
from core.table import Table
from core.query import Query

class TracksTable(Table):
    def __init__(
        self,
        cursor: Cursor,
        query_builder: Query
    ) -> None:
        super().__init__(
            cursor = cursor,
            query_builder = query_builder
        )

        self.name = "tracks"
        self.fields = [
            "access",
            "artwork_url",
            "created_at",
            "description",
            "duration",
            "id",
            "metadata_artist",
            "permalink_url",
            "playback_count",
            "stream_url",
            "title",
            "uri",
            "urn",
        ]
