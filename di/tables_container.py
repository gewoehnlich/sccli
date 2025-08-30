from dependency_injector import containers, providers
from tables.tracks import TracksTable
from tables.users import UsersTable


class TablesContainer(containers.DeclarativeContainer):
    tracks = providers.Callable(TracksTable)
    users = providers.Callable(UsersTable)
