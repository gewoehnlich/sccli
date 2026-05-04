from typing import Callable
from sqlalchemy.orm import Session

from di.models_container import ModelsContainer
from repositories.account_repository import AccountRepository
from repositories.track_repository import TrackRepository
from repositories.user_repository import UserRepository


class RepositoriesContainer:
    def __init__(
        self,
        models: ModelsContainer,
        session_factory: Callable[[], Session],
    ) -> None:
        self.account = AccountRepository(
            model=models.account,
            session_factory=session_factory,
        )

        self.track = TrackRepository(
            model=models.track,
            session_factory=session_factory,
        )

        self.user = UserRepository(
            model=models.user,
            session_factory=session_factory,
        )
