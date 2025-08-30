from core.di_container import DiContainer
from tables.tracks import TracksTable
from tables.users import UsersTable


class TablesContainer(DiContainer):
    def __init__(self) -> None:
        self.tracks = TracksTable
        self.users = UsersTable
