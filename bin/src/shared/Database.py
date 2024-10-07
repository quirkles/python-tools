import sqlite3
from os import path
from typing import List

from src.store.Datastore import home_dir


class Database:
    def __init__(self, db_name: str):
        self.db_name = db_name
        # Check that a db file exists in the home directory
        home_dir = path.expanduser("~")
        datastore_path = path.join(home_dir, f".{db_name}.db")
        self.db = sqlite3.connect(datastore_path)
        self.cursor = self.db.cursor()

    def create_table(self, table_name: str, columns: List[str]):
        self.cursor.execute(f"""CREATE TABLE {table_name} ({', '.join(columns)}, id INTEGER PRIMARY KEY)
        """)

    def insert(self, table_name: str, dict_values: dict):
        # First lets check that the table exists and create it if it doesn't
        self.cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}'")
        if not self.cursor.fetchone():
            self.create_table(table_name, [f"{key}" for key, value in dict_values.items()])
            # add an auto incrementing id column
        sql = f"INSERT INTO {table_name}({', '.join(dict_values.keys())}) VALUES({', '.join(['?' for _ in dict_values.values()])})"

        self.cursor.execute(sql, list(dict_values.values()))
        self.commit()

    def select(self, table_name: str, columns: List[str]):
        self.cursor.execute(f"SELECT {', '.join(columns)} FROM {table_name}")

    def commit(self):
        self.db.commit()

    def list_all(self, table_name: str):
        self.cursor.execute(f"SELECT * FROM {table_name}")
        return self.cursor.fetchall()

    def close(self):
        self.db.close()
