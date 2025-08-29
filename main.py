from dotenv import load_dotenv
from sqlite3 import Connection, Cursor
from core.query import Query
from core.shell import shell
from core.database import Database
from player.player import Player
from tables.tracks import TracksTable
from tables.users import UsersTable
from utils.stop import stop


# def initialize_db() -> Cursor:
#     db: Connection = Database()
#     cursor: Cursor = db.cursor
#
#     db.create_table_if_not_exists(
#         table = TracksTable(
#             cursor = cursor,
#             query_builder = query_builder,
#         )
#     )
#
#     db.create_table_if_not_exists(
#         table = UsersTable(
#             cursor = cursor,
#             query_builder = query_builder,
#         )
#     )
#
#     return cursor

if __name__ == "__main__":
    # load .env file variables
    load_dotenv()

    # database connection
    query_builder: Query = Query()

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
    shell()
