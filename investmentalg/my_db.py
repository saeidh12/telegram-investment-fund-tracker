import sqlite3

class MyDB:
    def __init__(self, db_file):
        self._db = sqlite3.connect(db_file)