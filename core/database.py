import sqlite3

class Database:
    _DATABASE_NAME = "sccli.db"
    _FIELDS_SEPARATOR = ", "

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Database, cls).__new__(cls)

        return cls._instance

    def __init__(self):
        self.db: sqlite3.Connection = sqlite3.connect(self._DATABASE_NAME)
        self.cursor: sqlite3.Cursor = self.db.cursor()

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
        query: str = self._make_query(
            statement = "CREATE TABLE IF NOT EXISTS",
            table = table,
            fields = fields
        )

        self.cursor.execute(query)

    def _make_query(
        self,
        statement: str,
        table: str,
        fields: list[str]
    ) -> str:
        fields_string: str = self._concatenate_fields(fields = fields)

        query: str = f"{statement} {table}({fields_string})"
        return query

    def _concatenate_fields(
        self,
        fields: list[str]
    ) -> str:
        fields_string: str = str()

        for field in fields:
            fields_string += field + self._FIELDS_SEPARATOR 

        if fields_string.endswith(self._FIELDS_SEPARATOR):
            fields_string = fields_string.rstrip(self._FIELDS_SEPARATOR)

        return fields_string
