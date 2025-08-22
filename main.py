from dotenv import load_dotenv
from sqlite3 import Connection
from src.core.shell import shell
from src.core.database import Database
from src.player.player import Player

if __name__ == "__main__":
    # load .env file variables
    load_dotenv()

    # database connection
    db: Database = Database()
    cur: Connection = db.cursor

    # # cli music player
    # player: Player = Player()
    # player.run()

    # start shell session
    shell()
