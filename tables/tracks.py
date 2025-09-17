from core.table import Table


class TracksTable(Table):
    name: str = "tracks"
    fields: tuple[str] = (
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
    )
