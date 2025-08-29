import sqlite3
from core.table import Table
from core.query import Query


class Database:
    _DATABASE_NAME: str = "sccli.db"
    _instance = None

    def __new__(
        cls: object, 
        query_builder: Query,
    ) -> None:
        if cls._instance is None:
            cls._instance = super(
                Database, cls
            ).__new__(cls)

            cls._instance.query_builder = query_builder

        return cls._instance

    def __init__(
        self,
        query_builder: Query,
    ) -> None:
        if hasattr(self, "db"):
            return

        self.db: sqlite3.Connection = sqlite3.connect(self._DATABASE_NAME)
        self.cursor: sqlite3.Cursor = self.db.cursor()
        self.query_builder = query_builder

    def create_table_if_not_exists(
        self,
        table: Table
    ) -> None:
        name: str = table.name
        fields: list[str] = table.fields

        query: str = self.query_builder.make_query(
            statement = "CREATE TABLE IF NOT EXISTS",
            table = name,
            fields = fields
        )

        self.cursor.execute(query)
