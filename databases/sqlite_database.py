import sqlalchemy

from core.database import Database
from core.model import Model


class SqliteDatabase(Database):
    def __init__(
        self,
        database_name: str,
        base_model: type[Model] = Model,
    ) -> None:
        super().__init__(
            database_name=database_name,
            base_model=base_model,
            engine=sqlalchemy.create_engine(
                f"sqlite+pysqlite:///{ database_name }"
            )
        )
