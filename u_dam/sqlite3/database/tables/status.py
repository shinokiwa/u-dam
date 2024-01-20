"""
U-DAM管理テーブル
"""
from typing import Union
import enum
from sqlite3 import Connection


def create_table (conn:Connection) -> None:
    """
    テーブルを作成
    """
    conn.executescript((
        "CREATE TABLE udam_status ("
            "key TEXT PRIMARY KEY,"     # ステータスキー
            "value TEXT"                # ステータス値
        ");"
    ))


class UdamStatusKeys(enum.Enum):
    """
    頻出するステータスキーの定義
    """

    VERSION = 'version'
    UDAM_VERSION = 'udam_version'


def set_udam_status (conn:Connection, key:Union[str, UdamStatusKeys], value:str) -> None:
    """
    U-DAM管理テーブルにデータを保存する。

    - すでに存在するキーの場合は更新する。

    Args:
        conn (Connection): DBコネクション
        key (Union[str, StatusKeys]): キー名
        value (str): ステータス値
    """
    if isinstance(key, UdamStatusKeys):
        key = key.value

    sql = (
        "INSERT INTO udam_status (key, value) VALUES (?, ?)"
        "ON CONFLICT(key) DO UPDATE SET value = ?"
    )
    conn.execute(sql, (key, value, value))
    return


def get_udam_status (conn:Connection, key:Union[str, UdamStatusKeys]) -> str:
    """
    U-DAM管理テーブルからデータを取得する。

    Args:
        conn (Connection): DBコネクション
        key (Union[str, StatusKeys]): キー名

    Returns:
        str: データベース状態情報 (存在しない場合はNone)
    """
    if isinstance(key, UdamStatusKeys):
        key = key.value

    sql = "SELECT value FROM udam_status WHERE key = ?"
    row = conn.execute(sql, (key,)).fetchone()
    if row is None:
        return None
    else:
        return row[0]


def delete_udam_status (conn: Connection, key:Union[str, UdamStatusKeys]) -> None:
    """
    U-DAM管理テーブルからデータを削除する。

    Args:
        conn (Connection): DBコネクション
        key (Union[str, StatusKeys]): キー名
    """
    if isinstance(key, UdamStatusKeys):
        key = key.value

    sql = "DELETE FROM udam_status WHERE key = ?"
    conn.execute(sql, (key,))
    return

#### 頻出するステータスキーの関数化 ####

def set_udam_database_version (conn:Connection, version:int) -> None:
    """
    バージョンを設定
    """
    set_udam_status(conn, UdamStatusKeys.VERSION, str(version))
    return

def get_udam_database_version (conn:Connection) -> int:
    """
    バージョンを取得
    """
    return int(get_udam_status(conn, UdamStatusKeys.VERSION))