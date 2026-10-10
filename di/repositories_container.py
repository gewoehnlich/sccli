from typing import Callable
from sqlalchemy.orm import Session

from core.database import Database
from di.models_container import ModelsContainer
from repositories.account_repository import AccountRepository
from repositories.track_repository import TrackRepository
from repositories.user_repository import UserRepository


class RepositoriesContainer:
    def __init__(
        self,
        models: ModelsContainer,
        database: Database,
    ) -> None:
        self.account = AccountRepository(
            model=models.account,
            database=database,
        )

        self.track = TrackRepository(
            model=models.track,
            database=database,
        )

        self.user = UserRepository(
            model=models.user,
            database=database,
        )
