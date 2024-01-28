"""
u_dam.sqlite3.utils.migration のテスト
"""
import pytest
from pytest_mock import MockerFixture

import sqlite3
from pathlib import Path

from u_dam.sqlite3.utils.migration import *
from u_dam.sqlite3.utils.create import create_database
from u_dam.sqlite3.database.tables.status import UdamStatusKeys

def test_regexp():
    """
    正規表現のテスト
    """
    matches = regexp.match('v1_test.py')
    assert matches is not None
    assert matches.group(1) == "1"

    matches = regexp.match('v2.py')
    assert matches is not None
    assert matches.group(1) == "2"

    matches = regexp.match('v3_.py')
    assert matches is not None
    assert matches.group(1) == "3"

    matches = regexp.match('v1_test')
    assert matches is None

    matches = regexp.match('v1_test.py.bak')
    assert matches is None

    matches = regexp.match('v1test.py')
    assert matches is None

    matches = regexp.match('v_test.py')
    assert matches is None

    matches = regexp.match('av1_test.py')
    assert matches is None


def test_do_migration (mocker:MockerFixture):
    """
    do_migration
    
    it:
        - マイグレーションを実行する。
        - やや結合テスト気味になるが、load_migration_scriptsとrun_migration_scriptsのテストも兼ねる。
    """
    conn = sqlite3.connect("file:memdb1?mode=memory&cache=shared")
    conn = create_database(sqlite3.connect, "file:memdb1?mode=memory&cache=shared", "samples.p001_basic")
    do_migration(conn, 'samples.p001_basic', UdamStatusKeys.VERSION, 1)


    # バージョンが4になっていることを確認
    r = conn.execute('SELECT value FROM udam_status WHERE key="version" ').fetchone()
    assert r[0] == "4"

    # バージョン2適用確認 pagesテーブルが存在すること
    r = conn.execute('SELECT name FROM sqlite_master WHERE type="table" AND name="pages"').fetchone()
    assert r[0] == "pages"

    # バージョン3適用確認 pageテーブルにtitleカラムが追加されていることを確認
    # 単にクエリを実行して、エラーが出なければOKとする
    r = conn.execute('SELECT age FROM users').fetchall()
    assert r == []

    # バージョン4は故意に何もしないので確認不要

    # もう一度実行すると、max_versionを超えるので何もしない
    do_migration(conn, 'samples.p001_basic', UdamStatusKeys.VERSION, 4)
    r = conn.execute('SELECT value FROM udam_status WHERE key="version" ').fetchone()
    assert r[0] == "4"

    # max_versionがNoneの場合は、バージョン5が適用される
    mocker.patch('samples.p001_basic.UDAM_PARAMS.max_version', None)
    do_migration(conn, 'samples.p001_basic', UdamStatusKeys.VERSION, 4)
    r = conn.execute('SELECT value FROM udam_status WHERE key="version" ').fetchone()
    assert r[0] == "5"

    conn.close()