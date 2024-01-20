"""
connect_databaseをテスト用にモック化する
"""
from sqlite3 import Connection

from yt_diffuser.database import connect_database as _connect_database
from yt_diffuser.database.utils.init import init_database

def connect_database_with_init (db_file = None) -> Connection:
    """
    テスト用のDBをセットアップする。

    - 引数を指定しない場合はインメモリDBをセットアップする。
    - このメソッドではDBの初期化を行う。
    """
    conn = connect_database(db_file)
    init_database(conn, 1)

    return conn