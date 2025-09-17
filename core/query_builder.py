from typing import Self

from core.table import Table


class QueryBuilder:
    _FIELDS_SEPARATOR: str = ", "

    _instance:    Self | None = None
    _initialized: bool        = False

    def __new__(
        cls: type[Self],
        *args,
        **kwargs
    ) -> Self:
        if cls._instance is None:
            cls._instance = super().__new__(cls)

        return cls._instance

    def __init__(
        self
    ) -> None:
        if not self._initialized:
            self._initialized = True

    def make_query(
        self,
        statement: str,
        table:     Table,
        values:    tuple[str] | None = None
    ) -> str:
        fields_string: str = self._concatenate_fields(fields = table.fields)
        query:         str = f"{statement} {table.name}({fields_string})"
        if values:
            values_string: str = self._concatenate_fields(fields = values)
            query += f" VALUES({values_string})"

        return query

    def _concatenate_fields(
        self,
        fields: tuple[str]
    ) -> str:
        fields_string: str = ""

        for field in fields:
            fields_string += str(field) + self._FIELDS_SEPARATOR

        if fields_string.endswith(self._FIELDS_SEPARATOR):
            fields_string = fields_string.rstrip(self._FIELDS_SEPARATOR)

        return fields_string
