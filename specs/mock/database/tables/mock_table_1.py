"""
テスト用モックテーブル1
"""
from sqlite3 import Connection

def create_table (conn:Connection):
    conn.execute("""
        CREATE TABLE mock_table_1 (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            value INTEGER NOT NULL
        )
    """)
