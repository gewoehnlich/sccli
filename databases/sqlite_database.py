from sqlalchemy.orm import sessionmaker
import sqlalchemy

from core.database import Database
from di.models_container import ModelsContainer


class SqliteDatabase(
    Database
):
    def __init__(
        self,
        database_name: str,
        models:        ModelsContainer,
    ) -> None:
        print(database_name)
        self.database_name: str = database_name

        self.engine: sqlalchemy.Engine = sqlalchemy.create_engine(
            f"sqlite+pysqlite:///{ self.database_name }"
        )

        self.session_factory = sessionmaker(
            bind = self.engine,
            expire_on_commit = False,
        )

        self.models: ModelsContainer = models


    def initialize_tables(
        self,
    ) -> None:
        self.models.model().metadata.create_all(self.engine)
