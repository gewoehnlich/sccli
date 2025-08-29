from core.table import Table
from core.request import Request


class Action:
    def run(
        self, 
        # request: Request,
        table: Table | None = None,
    ) -> bool:
        return True
