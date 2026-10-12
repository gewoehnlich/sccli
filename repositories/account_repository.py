from core.database import Database
from core.repository import Repository
from models.account import Account


class AccountRepository(Repository[Account]):
    model = Account

    def __init__(
        self,
        database: Database,
    ) -> None:
        super().__init__(
            database=database,
        )
