from dependency_injector import containers, providers

from core.database import Database
from databases.sqlite_database import SqliteDatabase


class DatabaseContainer(
    containers.DeclarativeContainer
):
    sqlite = providers.Singleton(
        SqliteDatabase,
    )
