"""DB操作を行うモジュール
"""
import sqlite3
import datetime
from typing import Union
from os import PathLike
from pathlib import Path

def connect_database(file_path:Union[str, bytes, PathLike, Path]) -> sqlite3.Connection:
    """データベースに接続する

    Args:
        file_path (Union[str, bytes, PathLike, Path]): データベースファイルパス
    """
    if isinstance(file_path, (PathLike, Path)):
        file_path = str(file_path)

    conn = sqlite3.connect(file_path)
    conn.row_factory = sqlite3.Row

    sqlite3.register_adapter(datetime.date, adapt_date)
    sqlite3.register_adapter(datetime.datetime, adapt_datetime)

    sqlite3.register_converter("date", convert_date)
    sqlite3.register_converter("datetime", convert_datetime)
    sqlite3.register_converter("timestamp", convert_timestamp)

    return conn


def adapt_date(val:datetime.date):
    """ datetime.date を timezone-naive ISO 8601 date に変換する
    """
    return val.isoformat()

def adapt_datetime(val:datetime.datetime):
    """ datetime.datetime を timezone-naive ISO 8601 datetime に変換する
    """
    return val.isoformat()

def convert_date(val:bytes):
    """ ISO 8601 date を datetime.date object に変換する
    """
    return datetime.date.fromisoformat(val.decode())

def convert_datetime(val:bytes):
    """ ISO 8601 datetime を datetime.datetime object に変換する
    """
    return datetime.datetime.fromisoformat(val.decode())

def convert_timestamp(val:bytes):
    """ timestamp を datetime.datetime object に変換する
    """
    return datetime.datetime.fromtimestamp(int(val))

