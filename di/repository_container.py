from sqlalchemy.orm import Session, sessionmaker

from di.models_container import ModelsContainer
from repositories.account_repository import AccountRepository
from repositories.track_repository import TrackRepository


class RepositoryContainer:
    def __init__(
        self,
        models: ModelsContainer,
        session_factory: type[Session],
    ) -> None:
        self.account = AccountRepository(
            model=models.account,
            session_factory=session_factory,
        )

        self.track = TrackRepository(
            model=models.track,
            session_factory=session_factory,
        )
