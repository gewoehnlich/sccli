from typing import Callable
import sqlalchemy
from sqlalchemy.orm import Session, sessionmaker
from core.model import Model


class Database:
    def __init__(
        self,
        database_name: str,
        engine: sqlalchemy.Engine,
        base_model: type[Model] = Model,
    ) -> None:
        self.database_name: str = database_name

        self.engine: sqlalchemy.Engine = engine
        self.session_factory: Callable[[], Session] = sessionmaker(
            bind=self.engine,
            expire_on_commit=False,
        )

        self.base_model: type[Model] = base_model

    def initialize_tables(
        self,
    ) -> None:
        """Create tables that are not present yet"""
        self.base_model().metadata.create_all(self.engine)
