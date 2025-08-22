import sqlite3

class Database:
    def __init__(self):
        DATABASE_NAME = "sccli.db"

        self.db: sqlite3.Connection = sqlite3.connect(DATABASE_NAME)
        self.cursor: sqlite3.Cursor = self.db.cursor()
