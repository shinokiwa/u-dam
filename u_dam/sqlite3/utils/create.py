"""
DBの初期化を行うモジュール
"""
from typing import Callable
import sqlite3
from importlib import import_module

from logging import getLogger; logger = getLogger(__name__)

from .types import StrOrBytesOrPath
from .connection import connect_database
from .params import (
    UdamParams,
    get_udam_params
)
from ..database.tables.status import (
    set_udam_database_version,
    set_udam_database_udam_version,
)

def create_database (
        connection_method:Callable[[StrOrBytesOrPath], sqlite3.Connection],
        database_path: StrOrBytesOrPath,
        package_name:str
    ) -> sqlite3.Connection:
    """
    DBの初期化を行う。この関数は、存在していないDBを作成する場合に使用する。

    - package_name で指定されたパッケージにあるテーブルを全て作成する。
    - パッケージの__init__.pyで、UDAM_PARAMSで指定されたテーブルを全て作成する。
    - UDAM_PARAMSの設定は、ドキュメントやサンプルを参照のこと。
    - インメモリDBを作成する場合は、database_pathに"file:memdb1?mode=memory&cache=shared"を指定する必要がある。

    params:
        connection_method: DB接続を行う関数。DBのパスを引数にして、Connectionを返す必要がある。
                           特別な指定がなければ、sqlite3.connectを指定してよい。
        database_path: DBのパス
        package_name: テーブルを作成するパッケージ名
    """
    logger.debug(f"create_database: {database_path}")
    conn = connection_method(database_path)
    params =init_database(conn, package_name)
    conn.commit()

    # U-DAM自身のテーブルを作成
    create_udam_database(database_path).close()

    # バージョンを設定
    set_udam_database_version(conn, params.version)
    conn.commit()

    return conn

def create_udam_database (database_path: StrOrBytesOrPath) -> sqlite3.Connection:
    """
    U-DAM自身のDBを作成する。
    """
    logger.debug(f"create_udam_database: {database_path}")
    conn = connect_database(database_path)
    udam_params = init_database(conn, "u_dam.sqlite3.database")
    # バージョンを設定
    set_udam_database_udam_version(conn, udam_params.version)
    conn.commit()
    return conn


def init_database (conn:sqlite3.Connection, package_name:str) -> UdamParams:
    """
    DBの初期化の実体処理。

    - U-DAM自身のテーブルも作成するので、実体を分離している。
    """
    params = get_udam_params(package_name)

    if params.auto_initialize_package is None:
        tables = package_name
    else:
        tables = f"{package_name}.{params.auto_initialize_package}"
    
    logger.debug(f"auto_initialize_package: {tables}")

    # テーブルを作成
    for table_name in params.auto_initialize_tables:

        try:
            table = import_module(f"{tables}.{table_name}")
        except ModuleNotFoundError as e:
            raise Exception(f"No table module named '{tables}.{table_name}'") from e

        if hasattr(table, params.create_table):
            logger.debug(f"create table at package: {tables}.{table_name}")
            getattr(table, params.create_table)(conn)
    
    return params
