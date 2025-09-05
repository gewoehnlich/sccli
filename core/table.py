class Table:
    name: str = ""
    fields: tuple[str] = tuple()

    def __str__(self) -> str:
        return self.name
