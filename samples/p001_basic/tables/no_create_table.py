"""
create_tableメソッドが存在しないモジュールは実行されない。
"""
from sqlite3 import Connection


def create_table_1 (conn:Connection) -> None:
    """
    テーブルを作成
    """
    conn.executescript((
        "CREATE TABLE users ("
            "user_id INTEGER PRIMARY KEY AUTOINCREMENT,"     # ユーザーID
            "name TEXT"                                      # 名前
        ");"
    ))


