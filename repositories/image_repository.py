from core.database import Database
from core.repository import Repository
from models.image import Image


class ImageRepository(Repository[Image]):
    model = Image

    def __init__(
        self,
        database: Database,
    ) -> None:
        super().__init__(
            database=database,
        )
