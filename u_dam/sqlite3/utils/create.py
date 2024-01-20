"""
DBの初期化を行うモジュール
"""
from os import PathLike
from typing import Callable, Union
from pathlib import Path
import sqlite3
from importlib import import_module

from logging import getLogger; logger = getLogger(__name__)

from .connection import connect_database
from .params import UdamParams
from ..database.tables.status import (
    UdamStatusKeys,
    set_udam_status,
)

def create_database (
        connection_method:Callable[[Union[str, bytes, PathLike, Path]], sqlite3.Connection],
        database_path: Union[str, bytes, PathLike, Path],
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
    conn = connection_method(database_path)
    params =init_database(conn, package_name, UdamStatusKeys.VERSION)
    conn.commit()

    # U-DAM自身のテーブルを作成
    udam_conn =connect_database(database_path)
    udam_params = init_database(udam_conn, "u_dam.sqlite3.database", UdamStatusKeys.UDAM_VERSION)

    # バージョンを設定
    set_udam_status(udam_conn, UdamStatusKeys.UDAM_VERSION, udam_params.version)
    set_udam_status(udam_conn, UdamStatusKeys.VERSION, params.version)
    udam_conn.commit()
    udam_conn.close()

    return conn



def init_database (conn:sqlite3.Connection, package_name:str, version_key:UdamStatusKeys) -> UdamParams:
    """
    DBの初期化の実体処理。

    - U-DAM自身のテーブルも作成するので、実体を分離している。
    """
    try:
        package = import_module(package_name)
    except ModuleNotFoundError as e:
        raise Exception(f"No package named '{package_name}'") from e

    if not hasattr(package, 'UDAM_PARAMS'):
        raise Exception(f"UDAM_PARAMS is not defined in {package_name}")
    
    params:UdamParams = package.UDAM_PARAMS
    if not isinstance(params, UdamParams):
        raise Exception(f"UDAM_PARAMS is not UdamParams in {package_name}")

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
