from collections.abc import Generator
from contextlib import contextmanager

import sqlalchemy
from alembic import command
from alembic.config import Config as AlembicConfig
from sqlalchemy.orm import Session, sessionmaker


class Database:
    def __init__(
        self,
        engine: sqlalchemy.Engine,
        alembic_config: AlembicConfig,
    ) -> None:
        self._engine: sqlalchemy.Engine = engine

        self._sessions: sessionmaker[Session] = sessionmaker(
            bind=engine,
            expire_on_commit=False,
        )

        self._alembic_config: AlembicConfig = alembic_config

    def run_migrations(
        self,
    ) -> None:
        """Apply all pending migrations."""
        command.upgrade(self._alembic_config, "head")

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
