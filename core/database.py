from typing import Callable
import sqlalchemy
from sqlalchemy.orm import Session, sessionmaker
from core.model import Model


class Database:
    def __init__(
        self,
        name: str,
        engine: sqlalchemy.Engine,
    ) -> None:
        self.name: str = name

        self._engine: sqlalchemy.Engine = engine

        self.session_factory: Callable[[], Session] = sessionmaker(
            bind=self._engine,
            expire_on_commit=False,
        )

        self._base_model: type[Model] = Model

    def initialize_tables(
        self,
    ) -> None:
        """Create tables that are not present yet"""
        self._base_model().metadata.create_all(self._engine)
