from core.database import Database
from core.repository import Repository
from models.account import Account


class AccountRepository(Repository[Account]):
    def __init__(
        self,
        model: type[Account],
        database: Database,
    ) -> None:
        super().__init__(
            model=model,
            database=database,
        )
