from dependency_injector import containers, providers
from core.table import Table
from tables.tracks import TracksTable
from tables.users import UsersTable


class TablesContainer(containers.DeclarativeContainer):
    table_base = providers.Singleton(
        Table,
    )

    tracks = providers.Singleton(
        TracksTable,
    )
    users = providers.Singleton(
        UsersTable,
    )
