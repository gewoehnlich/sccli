from core.database import Database
from core.repository import Repository
from models.setting import Setting


class SettingRepository(Repository[Setting]):
    model = Setting

    def __init__(
        self,
        database: Database,
    ) -> None:
        super().__init__(
            database=database,
        )
