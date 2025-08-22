from dotenv import load_dotenv
import sqlite3
from src.core.shell import shell
from src.core.database import Database
from src.player.player import Player

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
