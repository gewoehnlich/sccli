from sqlite3 import Connection, Cursor
from dotenv import load_dotenv
from core.query_builder import QueryBuilder
from core.shell import Shell
from core.database import Database
from player.player import Player
from tables.tracks import TracksTable
from tables.users import UsersTable
from utils.stop import stop


if __name__ == "__main__":
    # load .env file variables
    load_dotenv()

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
    shell: Shell = Shell(
        actions = actions,
        commands = commands,
        db = db,
        requests = requests,
        tables = tables,
        query_builder = query_builder,
    )
