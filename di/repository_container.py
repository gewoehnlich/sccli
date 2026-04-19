from sqlalchemy.orm import Session, sessionmaker

from repositories.account_repository import AccountRepository
from repositories.track_repository import TrackRepository


class RepositoryContainer(

):
    def __init__(
        self,
        session_factory: sessionmaker[Session],
    ) -> None:
        self.account = AccountRepository(
            session_factory = session_factory,
        )

        self.track = TrackRepository(
            session_factory = session_factory,
        )
