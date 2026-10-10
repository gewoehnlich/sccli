import sqlite3
from pathlib import Path

from sqlalchemy import Engine, create_engine, event
from sqlalchemy.engine import URL
from sqlalchemy.pool import ConnectionPoolEntry

from core.database import Database
from di.models_container import ModelsContainer


class SqliteDatabase(Database):
    def __init__(
        self,
        path: Path,
        models: ModelsContainer,
    ) -> None:
        super().__init__(
            engine=self._create_engine(path),
            models=models,
        )

    def _create_engine(
        self,
        path: Path,
    ) -> Engine:
        path.parent.mkdir(parents=True, exist_ok=True)
        engine = create_engine(URL.create("sqlite+pysqlite", database=str(path)))
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
