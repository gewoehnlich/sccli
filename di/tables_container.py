from dependency_injector import containers, providers

from core.table          import Table
from tables.tracks_table import TracksTable
from tables.users_table  import UsersTable


class TablesContainer(
    containers.DeclarativeContainer
):
    table_base = providers.Singleton(
        Table,
    )

    tracks = providers.Singleton(
        TracksTable,
    )
    users = providers.Singleton(
        UsersTable,
    )
