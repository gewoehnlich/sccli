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
        database: Database,
    ) -> None:
        self.account = AccountRepository(
            database=database,
        )

        self.track = TrackRepository(
            database=database,
        )

        self.user = UserRepository(
            database=database,
        )
