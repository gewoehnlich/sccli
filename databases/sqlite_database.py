import sqlite3
from pathlib import Path

from alembic.config import Config as AlembicConfig
from sqlalchemy import Engine, create_engine, event
from sqlalchemy.engine import URL
from sqlalchemy.pool import ConnectionPoolEntry

from core.database import Database


class SqliteDatabase(Database):
    def __init__(
        self,
        path: Path,
        alembic_config: AlembicConfig,
    ) -> None:
        super().__init__(
            engine=self._create_engine(path),
            alembic_config=alembic_config,
        )

    def _create_engine(
        self,
        path: Path,
    ) -> Engine:
        engine: Engine = create_engine(
            URL.create("sqlite+pysqlite", database=str(path))
        )
        event.listen(engine, "connect", self._configure)

        return engine

    def _configure(
        self,
        dbapi_connection: sqlite3.Connection,
        _: ConnectionPoolEntry,
    ) -> None:
        cursor = dbapi_connection.cursor()

        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.execute("PRAGMA busy_timeout=5000")

        cursor.close()
