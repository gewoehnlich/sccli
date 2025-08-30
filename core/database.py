import sqlite3
from typing import Any

from core.table import Table
from core.query_builder import QueryBuilder
from di.tables_container import TablesContainer


class Database:
    DATABASE_NAME: str = "sccli.db"

    _instance = None

    def __new__(cls: object) -> None:
        if cls._instance is None:
            cls._instance = super().__new__(cls)

        return cls._instance

    def __init__(
        self,
        db: str,
        tables: TablesContainer,
        query_builder: QueryBuilder,
    ) -> None:
        if db != "SQLITE":
            raise Exception("not supported db; to-do")

        self.db: sqlite3.Cursor = sqlite3.connect(self.DATABASE_NAME).cursor()
        self.tables: TablesContainer = tables
        self.query_builder = query_builder

    def create_table_if_not_exists(
        self,
        table: Table
    ) -> None:
        query: str = self.query_builder.make_query(
            statement = "CREATE TABLE IF NOT EXISTS",
            table = table.name,
            fields = table.fields
        )

        self.db.execute(query)

    def insert(
        self,
        table: Table,
        data: dict[str, Any],
    ) -> None:
        result: list[str] = []
        for field in table.fields:
            result.append(
                data.get(field, "")
            )

        query: str = self.query_builder.make_query(
            statement = "INSERT INTO",
            table = table.name,
            fields = result,
        )

        self.db.execute(query)
