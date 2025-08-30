class QueryBuilder:
    _FIELDS_SEPARATOR = ", "

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(QueryBuilder, cls).__new__(cls)

        return cls._instance

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
        fields_string: str = str()

        for field in fields:
            fields_string += field + self._FIELDS_SEPARATOR

        if fields_string.endswith(self._FIELDS_SEPARATOR):
            fields_string = fields_string.rstrip(self._FIELDS_SEPARATOR)

        return fields_string
