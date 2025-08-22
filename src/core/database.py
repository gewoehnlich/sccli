import sqlite3

class Database:
    def __init__(self):
        DATABASE_NAME = "sccli.db"

        self.db = sqlite3.connect(DATABASE_NAME)
        self.cursor = self.db.cursor()
