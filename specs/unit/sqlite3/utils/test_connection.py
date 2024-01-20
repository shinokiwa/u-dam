"""
u-dam.sqlite3.utils.connection のテスト
"""
import pytest

import sqlite3
import datetime
import tempfile
from pathlib import Path

from u_dam.sqlite3.utils.connection import *

def test_connect_database():
    """
    connect_database

    it:
        - データベースに接続する。
    """
    conn = connect_database(":memory:")
    assert isinstance(conn, sqlite3.Connection)
    conn.close()

    file_path = tempfile.NamedTemporaryFile().name
    conn = connect_database(file_path)
    assert isinstance(conn, sqlite3.Connection)
    conn.close()

    file_path = Path(file_path)
    conn = connect_database(file_path)
    assert isinstance(conn, sqlite3.Connection)
    conn.close()


def test_adapt_date():
    """
    adapt_date

    it:
        - datetime.date を timezone-naive ISO 8601 date に変換する。
    """
    date = datetime.date.fromisoformat("2020-01-01")
    assert adapt_date(date) == "2020-01-01"

def test_adapt_datetime():
    """
    adapt_datetime

    it:
        - datetime.datetime を timezone-naive ISO 8601 datetime に変換する。
    """
    dt = datetime.datetime.fromisoformat("2020-01-01T00:00:00")
    assert adapt_datetime(dt) == "2020-01-01T00:00:00"

def test_convert_date():
    """
    convert_date

    it:
        - ISO 8601 date を datetime.date object に変換する。
    """
    date = datetime.date.today()
    iso_date = date.isoformat()
    assert convert_date(iso_date.encode()) == date

def test_convert_datetime():
    """
    convert_datetime

    it:
        - ISO 8601 datetime を datetime.datetime object に変換する。
    """
    dt = datetime.datetime.now()
    iso_dt = dt.isoformat()
    assert convert_datetime(iso_dt.encode()) == dt

def test_convert_timestamp():
    """
    convert_timestamp

    it:
        - timestamp を datetime.datetime object に変換する。
    """
    timestamp = datetime.datetime.now().timestamp()
    assert convert_timestamp(str(int(timestamp)).encode()) == datetime.datetime.fromtimestamp(int(timestamp))