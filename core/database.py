import sqlite3
from core.table import Table
from core.query import Query
from tables.tracks import TracksTable
from tables.users import UsersTable

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
            table = TracksTable()
        )

        self._create_table_if_not_exists(
            table = UsersTable()
        )

    def _create_table_if_not_exists(
        self,
        table: Table
    ) -> None:
        name: str = table.name
        fields: list[str] = table.fields

        query: str = self.query.make_query(
            statement = "CREATE TABLE IF NOT EXISTS",
            table = name,
            fields = fields
        )

        self.cursor.execute(query)

