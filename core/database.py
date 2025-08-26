import sqlite3
from core.query import Query

class Database:
    _DATABASE_NAME = "sccli.db"
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Database, cls).__new__(cls)

        return cls._instance

    def __init__(self):
        self.db: sqlite3.Connection = sqlite3.connect(self._DATABASE_NAME)
        self.cursor: sqlite3.Cursor = self.db.cursor()
        self.query = Query()

    def initialize_tables(self) -> None:
        self._create_table_if_not_exists(
            table = "tracks",
            fields = [
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
        )

        self._create_table_if_not_exists(
            table = "users",
            fields = [
                "avatar_url",
                "city",
                "country",
                "created_at",
                "description",
                "followers_count",
                "followings_count",
                "id",
                "kind",
                "last_modified",
                "permalink",
                "permalink_url",
                "plan",
                "track_count",
                "uri",
                "urn",
                "username",
            ]
        )

    def _create_table_if_not_exists(
        self,
        table: str,
        fields: list[str]
    ) -> None:
        query: str = self.query.make_query(
            statement = "CREATE TABLE IF NOT EXISTS",
            table = table,
            fields = fields
        )

        self.cursor.execute(query)

