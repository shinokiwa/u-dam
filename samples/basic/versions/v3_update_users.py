"""
version 3
Usersテーブルに、ageカラムを追加
"""
import sqlite3

def upgrade (conn:sqlite3.Connection) -> None:
    """
    バージョンアップ処理
    """
    conn.executescript((
        "ALTER TABLE users ADD COLUMN age INTEGER;"
    ))

def downgrade (conn:sqlite3.Connection) -> None:
    """
    バージョンダウン処理
    """
    conn.executescript((
        "ALTER TABLE users DROP COLUMN age;"
    ))
