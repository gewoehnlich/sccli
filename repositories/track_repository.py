from core.database import Database
from core.repository import Repository
from models.track import Track


class TrackRepository(Repository):
    def __init__(
        self,
        model: type[Track],
        database: Database,
    ) -> None:
        super().__init__(
            model=model,
            database=database,
        )
