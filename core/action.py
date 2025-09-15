from core.database import Database
from core.table import Table
from core.request import Request


class Action:
    request:  Request  | None = None
    database: Database | None = None
    table:    Table    | None = None

    def __init__(
        self,
        request:  Request  | None = None,
        database: Database | None = None,
        table:    Table    | None = None,
    ) -> None:
        if request:
            self.request = request

        if database:
            self.database = database

        if table:
            self.table = table

    def run(
        self,
    ) -> bool:
        return False
