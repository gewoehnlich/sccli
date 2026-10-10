from collections.abc import Generator
from contextlib import contextmanager

import sqlalchemy
from sqlalchemy.orm import Session, sessionmaker

from core.model import Model
from di.models_container import ModelsContainer


class Database:
    def __init__(
        self,
        engine: sqlalchemy.Engine,
        models: ModelsContainer,
    ) -> None:
        self._engine: sqlalchemy.Engine = engine

        self._sessions: sessionmaker[Session] = sessionmaker(
            bind=engine,
            expire_on_commit=False,
        )

        self._base_model: type[Model] = models.base

    def initialize_tables(
        self,
    ) -> None:
        """Create tables that are not present yet"""
        self._base_model().metadata.create_all(self._engine)

    @contextmanager
    def session(
        self,
    ) -> Generator[Session]:
        """Commit on success, roll back on error, always close."""
        with self._sessions.begin() as session:
            yield session

    def close(
        self,
    ) -> None:
        self._engine.dispose()
