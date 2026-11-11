import sqlite3
from pathlib import Path

from alembic.config import Config as AlembicConfig
from sqlalchemy import event
from sqlalchemy.engine import URL
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine
from sqlalchemy.pool import ConnectionPoolEntry

from core.database import Database


class SqliteDatabase(Database):
    def __init__(self, path: Path, alembic_config: AlembicConfig) -> None:
        super().__init__(
            engine=self._create_engine(path),
            alembic_config=alembic_config,
            migrations_url=URL.create(
                "sqlite+pysqlite", database=str(path)
            ).render_as_string(),
        )

    def _create_engine(self, path: Path) -> AsyncEngine:
        engine = create_async_engine(
            URL.create("sqlite+aiosqlite", database=str(path)),
        )
        event.listen(engine.sync_engine, "connect", self._configure)

        return engine

    def _configure(
        self, dbapi_connection: sqlite3.Connection, _: ConnectionPoolEntry
    ) -> None:
        # synchronous on purpose, exactly like your original
        cursor = dbapi_connection.cursor()

        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.execute("PRAGMA busy_timeout=5000")

        cursor.close()
