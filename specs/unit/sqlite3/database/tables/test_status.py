"""
u_dam.database.tables.status のテスト
"""
import pytest

import sqlite3

from u_dam.sqlite3.database.tables.status import *

@pytest.fixture(scope="function")
def conn():
    conn = sqlite3.connect(':memory:')
    conn.row_factory = sqlite3.Row

    create_table(conn)
    yield conn
    conn.close()

def test_create_table(conn:sqlite3.Connection):
    """
    create_status_table

    it:
        - ステータステーブルを作成する。
    """
    # SELECTにエラーが出なければOK
    result = conn.execute("SELECT COUNT(*) FROM udam_status").fetchone()
    assert result[0] == 0


def test_is_exist_table_udam_status(conn:sqlite3.Connection):
    """
    is_exist_table_udam_status

    it:
        - テーブルが存在しない場合はFalseを返す。
        - テーブルが存在する場合はTrueを返す。
    """
    assert is_exist_table_udam_status(conn) == True

    conn.execute("DROP TABLE udam_status")
    assert is_exist_table_udam_status(conn) == False


def test_set_udam_status(conn:sqlite3.Connection):
    """
    set_udam_status

    it:
        - データを挿入する。
        - すでに存在するキーの場合は更新する。
        - キー名は文字列でもStatusKeysでも指定できる。
    """

    set_udam_status(conn, 'version', "value")
    result = conn.execute("SELECT value FROM udam_status WHERE key = ?", ("version",)).fetchone()
    assert result['value'] == "value"

    set_udam_status(conn, UdamStatusKeys.VERSION, "value2")
    result = conn.execute("SELECT value FROM udam_status WHERE key = ?", ("version",)).fetchone()
    assert result['value'] == "value2"


def test_get_udam_status(conn):
    """
    get_status

    it:
        - キー名は文字列でもStatusKeysでも指定できる。
    """

    conn.execute("INSERT INTO udam_status (key, value) VALUES (?, ?)", ("version", "value"))

    result = get_udam_status(conn, "version")
    assert result == "value", "文字列で指定した場合"

    result = get_udam_status(conn, UdamStatusKeys.VERSION)
    assert result == "value", "StatusKeysで指定した場合"

    result = get_udam_status(conn, "key")
    assert result == None, "存在しないキーを指定した場合"


def test_delete_status(conn):
    """
    delete_udam_status

    it:
        - データを削除する。
        - キー名は文字列でもStatusKeysでも指定できる。
    """
    conn.execute("INSERT INTO udam_status (key, value) VALUES (?, ?)", ("version", "value"))

    delete_udam_status(conn, "version")
    result = conn.execute("SELECT value FROM udam_status WHERE key = ?", ("version",)).fetchone()
    assert result == None, "文字列で指定した場合"

    conn.execute("INSERT INTO udam_status (key, value) VALUES (?, ?)", ("version", "value"))

    delete_udam_status(conn, UdamStatusKeys.VERSION)
    result = conn.execute("SELECT value FROM udam_status WHERE key = ?", ("version",)).fetchone()
    assert result == None, "StatusKeysで指定した場合"


#### 頻出するステータスキーの関数化 ####
# ここからは上記メソッドに依存するので、上記メソッドのテストが通っていることが前提

def test_set_udam_database_version(conn):
    """
    set_udam_database_version

    it:
        - バージョンを設定する。
    """
    set_udam_database_version(conn, 1)
    result = get_udam_status(conn, "version")
    assert result == "1"

def test_get_udam_database_status(conn):
    """
    get_udam_database_version

    it:
        - バージョンを取得する。
    """
    set_udam_status(conn, "version", "1")
    result = get_udam_database_version(conn)
    assert result == 1