from sqlite3 import Connection, Cursor
from dotenv import load_dotenv
from core.di_container import DiContainer
from core.query_builder import QueryBuilder
from core.shell import shell
from core.database import Database
from player.player import Player
from tables.tracks import TracksTable
from tables.users import UsersTable
from utils.stop import stop


def main(di_container: DiContainer) -> None:
    # load .env file variables
    load_dotenv()

    # dependency injection
    # di_container: DiContainer = DiContainer()
    # di_container.wire(modules = [__name__])

    # database connection
    query_builder: QueryBuilder = QueryBuilder()

    db: Connection = Database(
        query_builder = query_builder
    )
    cursor: Cursor = db.cursor

    db.create_table_if_not_exists(
        table = TracksTable(
            cursor = cursor,
            query_builder = query_builder,
        )
    )

    db.create_table_if_not_exists(
        table = UsersTable(
            cursor = cursor,
            query_builder = query_builder,
        )
    )

    # # cli music player
    # player: Player = Player()
    # player.run()

    # start shell session
    shell(di_container = di_container)

if __name__ == "__main__":
    main(
        DiContainer()
    )
