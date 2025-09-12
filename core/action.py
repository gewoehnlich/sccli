from core.table import Table
from core.request import Request


class Action:
    request: Request | None = None
    table:   Table   | None = None

    def __init__(
        self,
        request: Request | None = None,
        table:   Table   | None = None,
    ) -> None:
        if request:
            self.request = request

        if table:
            self.table = table

    def run(
        self,
    ) -> bool:
        return False
