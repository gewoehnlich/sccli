from sqlite3 import Cursor
from typing import Any
from core.query_builder import QueryBuilder

class Table:
    name: str = str()
    fields: list[str] = list()

    def __init__(
        self,
        cursor: Cursor,
        query_builder: QueryBuilder,
    ) -> None:
        self.cursor: Cursor = cursor
        self.query_builder: QueryBuilder = query_builder

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
