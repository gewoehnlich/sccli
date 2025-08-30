from dependency_injector import containers, providers
from core.database import Database


class DatabaseContainer(containers.DeclarativeContainer):
    database = providers.Singleton(Database)
