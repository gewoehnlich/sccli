import sqlalchemy

from core.database import Database


class SqliteDatabase(Database):
    def __init__(
        self,
        name: str,
    ) -> None:
        super().__init__(
            name=name,
            engine=sqlalchemy.create_engine(f"sqlite+pysqlite:///{name}"),
        )
