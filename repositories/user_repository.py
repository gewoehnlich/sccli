from core.database import Database
from core.repository import Repository
from models.user import User


class UserRepository(Repository[User]):
    def __init__(
        self,
        model: type[User],
        database: Database,
    ) -> None:
        super().__init__(
            model=model,
            database=database,
        )
