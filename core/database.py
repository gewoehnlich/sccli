from __future__ import annotations
import sqlite3
from typing import Any, Self

from core.query_builder import QueryBuilder
from core.table import Table
from di.tables_container import TablesContainer


class Database:
    database_name: str = ""

    _instance: Self | None = None
    _initialized: bool = False

    def __new__(
        cls: type[Self],
        *args,
        **kwargs,
    ) -> Self:
        if cls._instance is None:
            cls._instance = super().__new__(cls)

        return cls._instance

    def __init__(
        self,
        database_name: str,
        tables:        TablesContainer,
        query_builder: QueryBuilder,
    ) -> None:
        if self._initialized:
            return None

        self.database_name = database_name
        self._db: sqlite3.Connection = sqlite3.connect(self.database_name)
        self.cursor = sqlite3.Cursor = self._db.cursor()
        self.tables: TablesContainer = tables
        self.query_builder: QueryBuilder = query_builder

        self._initialized = True

    def initialize_tables(self) -> None:
        for name, provider in self.tables.providers.items():
            table: Table = provider()

            self.create_table_if_not_exists(
                table = table
            )

    def create_table_if_not_exists(
        self,
        table: Table
    ) -> None:
        query: str = self.query_builder.make_query(
            statement = "CREATE TABLE IF NOT EXISTS",
            table = table.name,
            fields = table.fields
        )

        self.cursor.execute(query)

        self._db.commit()

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

        self.cursor.execute(query)

        self._db.commit()
