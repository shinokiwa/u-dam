"""
u_dam.sqlite3.setup のテスト
"""
import pytest

import sqlite3
import tempfile
from pathlib import Path

from u_dam.sqlite3 import (
    setup_database,
    get_udam_database_version
)

def test_setup_database ():
    """
    setup_database

    it:
        - データベースのセットアップを行う。
        - データベースファイルが存在しない場合は、ファイルおよびテーブルを作成する。
        - データベースファイルが存在する場合は、バージョンを確認し、必要に応じて更新する。
        - インメモリデータベースの場合は、テーブルを作成する。
        - インメモリDBを作成する場合は、database_pathに"file:memdb1?mode=memory&cache=shared"を指定する必要がある。

        - ほぼ結合テスト。
    """

    # インメモリDBの場合
    # :memory: は都合によりエラーになる
    #conn = setup_database(sqlite3.connect, ':memory:', 'samples.basic')

    # file:memdb1?mode=memory&cache=shared の場合
    conn = setup_database(sqlite3.connect, 'file:test_setup?mode=memory&cache=shared', 'samples.basic')
    
    tables = conn.execute('SELECT name FROM sqlite_master WHERE type="table" ORDER BY NAME ASC').fetchall()
    table_names = [table[0] for table in tables]
    assert table_names == [
        "pages",
        "sqlite_sequence",
        "udam_status",
        "users",
    ]
    assert get_udam_database_version(conn) == 4

    conn.close()

    # ファイルDBの場合
    # ファイルが存在しない場合
    db_path = tempfile.mkdtemp() + '/test.db'
    conn = setup_database(sqlite3.connect, db_path, 'samples.basic')

    tables = conn.execute('SELECT name FROM sqlite_master WHERE type="table" ORDER BY NAME ASC').fetchall()
    table_names = [table[0] for table in tables]
    assert table_names == [
        "pages",
        "sqlite_sequence",
        "udam_status",
        "users",
    ]
    assert get_udam_database_version(conn) == 4

    conn.close()

    # ファイルが既に存在する場合
    # udam_status のみ作成される
    exist_db_path = tempfile.mktemp()
    with sqlite3.connect(exist_db_path) as conn:
        from samples.basic.tables.users import create_table
        create_table(conn)

    conn = setup_database(sqlite3.connect, exist_db_path, 'samples.basic')

    tables = conn.execute('SELECT name FROM sqlite_master WHERE type="table" ORDER BY NAME ASC').fetchall()
    table_names = [table[0] for table in tables]
    assert table_names == [
        "pages",
        "sqlite_sequence",
        "udam_status",
        "users",
    ]
    assert get_udam_database_version(conn) == 4
    conn.close()

    # セットアップ済みの場合
    # 特に何もしないので、エラーがないことを確認する
    # 引数がPathの時に不具合があったので、ついでにここで確認
    conn = setup_database(sqlite3.connect, Path(db_path), 'samples.basic')
    assert get_udam_database_version(conn) == 4
    conn.close()
