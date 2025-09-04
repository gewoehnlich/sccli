class QueryBuilder:
    fields_separator: str | None = None

    _instance = None
    _initialized: bool = False

    def __new__(cls, *args, **kwargs) -> None:
        if cls._instance is None:
            cls._instance = super().__new__(cls)

        return cls._instance

    def __init__(
        self,
        fields_separator: str
    ) -> None:
        if not self._initialized:
            self.fields_separator = fields_separator
            self._initialized = True

    def make_query(
        self,
        statement: str,
        table: str,
        fields: tuple[str]
    ) -> str:
        fields_string: str = self._concatenate_fields(fields = fields)
        query: str = f"{statement} {table}({fields_string})"

        return query

    def _concatenate_fields(
        self,
        fields: tuple[str]
    ) -> str:
        fields_string: str = ""

        for field in fields:
            fields_string += field + self.fields_separator

        if fields_string.endswith(self.fields_separator):
            fields_string = fields_string.rstrip(self.fields_separator)

        return fields_string
