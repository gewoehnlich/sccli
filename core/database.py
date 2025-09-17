from __future__ import annotations
from typing import Any, Self
import sqlalchemy

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
        tables: TablesContainer,
    ) -> None:
        if self._initialized:
            return

        self.database_name: str = database_name
        self.engine: sqlalchemy.Engine = sqlalchemy.create_engine(
            f"sqlite+pysqlite:///{self.database_name}"
        )
        self.metadata: sqlalchemy.MetaData = sqlalchemy.MetaData()
        self.tables: TablesContainer = tables

        self._initialized = True


    def initialize_tables(
        self,
    ) -> None:
        for name, provider in self.tables.providers.items():
            table: Table = provider()

            self._map_to_sqlalchemy_table(
                table = table
            )

        self.metadata.create_all(self.engine)


    def _map_to_sqlalchemy_table(
        self,
        table: Table
    ) -> sqlalchemy.Table:
        columns: list[sqlalchemy.Column] = []
        for field in table.fields:
            columns.append(sqlalchemy.Column(field, sqlalchemy.String))

        return sqlalchemy.Table(table.name, self.metadata, *columns)


    def insert(
        self,
        table: Table,
        data: dict[str, Any],
    ) -> None:
        sqlalchemy_table = self.metadata.tables[table.name]
        statement = sqlalchemy.insert(sqlalchemy_table).values(**data)
        with self.engine.connect() as conn:
            conn.execute(statement)
            conn.commit()
