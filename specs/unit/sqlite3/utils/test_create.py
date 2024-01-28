"""
u_dam.sqlite3.utils.create のテスト
"""
import pytest
from pytest_mock import MockerFixture

from u_dam.sqlite3.utils.create import *

def test_create_database():
    """
    create_database
    
    it:
        - DBの初期化を行う。
        - package_name で指定されたパッケージにあるテーブルを全て作成する。
    """
    conn = create_database(connect_database, "file:memdb1?mode=memory&cache=shared", "samples.p001_basic")

    # アサーションの都合テーブルは名前順に並べ替える
    tables = conn.execute('SELECT name FROM sqlite_master WHERE type="table" ORDER BY NAME ASC').fetchall()
    table_names = [table[0] for table in tables]
    assert table_names == [
        "sqlite_sequence",
        "udam_status",
        "users",
    ]

    r = conn.execute('SELECT value FROM udam_status WHERE key="udam_version" ').fetchone()
    assert r is not None

    r = conn.execute('SELECT value FROM udam_status WHERE key="version" ').fetchone()
    assert r["value"] == "1"

    conn.close()

def test_create_udam_database():
    """
    create_udam_database
    
    it:
        - U-DAM自身のDBを作成する。
    """
    conn = create_udam_database("file:memdb1?mode=memory&cache=shared")

    # アサーションの都合テーブルは名前順に並べ替える
    tables = conn.execute('SELECT name FROM sqlite_master WHERE type="table" ORDER BY NAME ASC').fetchall()
    table_names = [table[0] for table in tables]
    assert table_names == [
        "udam_status"
    ]

    r = conn.execute('SELECT value FROM udam_status WHERE key="udam_version" ').fetchone()
    assert r is not None

    conn.close()



def test_errors_create_database (mocker:MockerFixture):
    """
    create_database のエラー系テスト
    """
    # 指定されたテーブルが存在しない
    with pytest.raises(Exception) as e:
        create_database(connect_database, "file:memdb1?mode=memory&cache=shared", "specs.database.error_no_tables")

    assert str(e.value) == "No table module named 'specs.database.error_no_tables.status'"