import sqlite3
from typing import List


class Database:
    def __init__(self, db_name: str):
        self.db_name = db_name
        self.db = sqlite3.connect(db_name)
        self.cursor = self.db.cursor()

    def create_table(self, table_name: str, columns: List[str]):
        self.cursor.execute(f"CREATE TABLE {table_name} ({', '.join(columns)})")

    def insert(self, table_name: str, values: List[str]):
        self.cursor.execute(f"INSERT INTO {table_name} VALUES ({', '.join(values)})")

    def select(self, table_name: str, columns: List[str]):
        self.cursor.execute(f"SELECT {', '.join(columns)} FROM {table_name}")

    def commit(self):
        self.db.commit()

    def close(self):
        self.db.close()
