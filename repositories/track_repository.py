from core.database import Database
from core.repository import Repository
from models.track import Track


class TrackRepository(Repository[Track]):
    model = Track

    def __init__(
        self,
        database: Database,
    ) -> None:
        super().__init__(
            database=database,
        )
