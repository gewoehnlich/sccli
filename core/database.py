import sqlite3
from core.table import Table
from core.query_builder import QueryBuilder


class Database:
    _DATABASE_NAME: str = "sccli.db"
    _instance = None

    def __new__(cls: object) -> None:
        if cls._instance is None:
            cls._instance = super().__new__(cls)

        return cls._instance

    def __init__(
        self,
        query_builder: QueryBuilder,
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

    def insert(
        self,
        data: dict[str, Any],
    ) -> None:
        result: list[str] = list()
        for field in self.fields:
            result.append(
                data.get(field, str())
            )

        query: str = self.query_builder.make_query(
            statement = "INSERT INTO",
            table = self.name,
            fields = result,
        )

        self.cursor.execute(query)
