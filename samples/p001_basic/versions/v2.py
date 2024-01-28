"""
version 2
pageテーブル追加
履歴名称はなくても問題なし。
"""
import sqlite3

def upgrade(conn: sqlite3.Connection):
    conn.executescript ((
        "CREATE TABLE pages ("
            "page_id INTEGER PRIMARY KEY AUTOINCREMENT,"     # ページID
            "name TEXT"                                      # 名前
        ");"
    ))

def downgrade(conn: sqlite3.Connection):
    conn.executescript ((
        "DROP TABLE pages;"
    ))