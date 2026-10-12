from core.database import Database
from core.repository import Repository
from models.user import User


class UserRepository(Repository[User]):
    model = User

    def __init__(
        self,
        database: Database,
    ) -> None:
        super().__init__(
            database=database,
        )
