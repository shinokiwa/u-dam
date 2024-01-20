"""
テスト用モックテーブル2
故意にcreate_tableを持たない
"""
from sqlite3 import Connection

def create__table (conn:Connection):
    conn.execute("""
        CREATE TABLE mock_table_1 (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            value INTEGER NOT NULL
        )
    """)
