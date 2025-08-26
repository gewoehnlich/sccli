from dotenv import load_dotenv
import sqlite3
from core.shell import shell
from core.database import Database
from player.player import Player
from utils.stop import stop

if __name__ == "__main__":
    # load .env file variables
    load_dotenv()

    # database connection
    db: sqlite3.Connection = Database()
    db.initialize_tables()

    cur: sqlite3.Cursor = db.cursor

    # # cli music player
    # player: Player = Player()
    # player.run()

    # start shell session
    shell()
