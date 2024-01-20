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
    conn = create_database(connect_database, "file:memdb1?mode=memory&cache=shared", "samples.basic")

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
    assert r["value"] == "2"

    conn.close()


def test_errors_create_database (mocker:MockerFixture):
    """
    create_database のエラー系テスト
    """

    # パッケージが存在しない
    with pytest.raises(Exception) as e:
        create_database(connect_database, "file:memdb1?mode=memory&cache=shared", "not_exists")
    
    assert str(e.value) == "No package named 'not_exists'"

    # UDAM_PARAMSが存在しない
    with pytest.raises(Exception) as e:
        create_database(connect_database, "file:memdb1?mode=memory&cache=shared", "specs.database.error_no_params")
    
    assert str(e.value) == "UDAM_PARAMS is not defined in specs.database.error_no_params"

    # UDAM_PARAMSがUdamParamsでない
    with pytest.raises(Exception) as e:
        create_database(connect_database, "file:memdb1?mode=memory&cache=shared", "specs.database.error_invalid_params")
    
    assert str(e.value) == "UDAM_PARAMS is not UdamParams in specs.database.error_invalid_params"

    # 指定されたテーブルが存在しない
    with pytest.raises(Exception) as e:
        create_database(connect_database, "file:memdb1?mode=memory&cache=shared", "specs.database.error_no_tables")
    
    assert str(e.value) == "No table module named 'specs.database.error_no_tables.status'"