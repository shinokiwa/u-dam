"""
データベースのセットアップを行う
"""
import logging; logger = logging.getLogger(__name__)
from typing import Callable, Tuple
import sqlite3
from pathlib import Path

from .types import StrOrBytesOrPath
from .migration import do_migration
from .connection import connect_database
from .create import (
    create_database,
    create_udam_database
)
from .params import (
    get_udam_params
)
from ..database.tables.status import (
    get_udam_database_version,
    set_udam_database_version,
    get_udam_database_udam_version,
    is_exist_table_udam_status,
    UdamStatusKeys
)

def setup_database (
    connection_method:Callable[[StrOrBytesOrPath], sqlite3.Connection],
    database_path: StrOrBytesOrPath,
    package_name:str
) -> sqlite3.Connection:
    """
    データベースのセットアップを行う。

    - データベースファイルが存在しない場合は、ファイルおよびテーブルを作成する。
    - データベースファイルが存在する場合は、バージョンを確認し、必要に応じて更新する。
    - インメモリデータベースの場合は、テーブルを作成する。
    - インメモリDBを作成する場合は、database_pathに"file:memdb1?mode=memory&cache=shared"を指定する必要がある。

    Args:
        connection_method: DB接続を行う関数。DBのパスを引数にして、Connectionを返す必要がある。
                           特別な指定がなければ、sqlite3.connectを指定してよい。
        database_path: DBのパス
        package_name: テーブルを作成するパッケージ名
    """

    # DBの作成が必要かどうかを判定
    is_need_create_db, is_need_create_table = is_need_create(database_path)

    init_conn = None
    if is_need_create_db:
        # DBを作成
        init_conn = create_database(connection_method, database_path, package_name)
    elif is_need_create_table:
        # テーブルを作成
        init_conn = create_udam_database(database_path)
        # バージョンを設定
        params = get_udam_params(package_name)
        set_udam_database_version(init_conn, params.initial_version)
        init_conn.commit()
    
    # U-DAM自身のマイグレーション
    with connect_database(database_path) as udam_conn:
        udam_version = get_udam_database_udam_version(udam_conn)
        do_migration(udam_conn, 'u_dam.sqlite3.database', UdamStatusKeys.UDAM_VERSION, udam_version)
    
    # マイグレーションを実行
    conn = connection_method(database_path)
    version = get_udam_database_version(conn)
    logger.debug(f"database migration: {database_path} version={version}")

    # マイグレーションスクリプトを実行
    do_migration(conn, package_name, UdamStatusKeys.VERSION, version)

    # ここまで接続を維持しないとインメモリDBの場合にデータベースが消える
    if init_conn is not None:
        init_conn.close()

    return conn


def is_need_create (database_path: StrOrBytesOrPath) -> Tuple[bool, bool]:
    """
    DBの作成が必要かどうかを判定する。

    - インメモリDBの場合は、常に作成が必要。
    - ファイルの存在を確認し、存在しない場合は作成が必要。
    - ファイルが存在し、かつ管理テーブルが存在しない場合は、管理テーブルのみ作成が必要。
    - ファイルが存在し、かつ管理テーブルが存在する場合は、作成は不要。

    Args:
        database_path (StrOrBytesOrPath): DBのパス

    Returns:
        Tuple[bool, bool]: (DBの作成が必要かどうか, 管理テーブルの作成が必要かどうか)
    """
    # 指定されたパスがインメモリかどうかを判定
    # str型かbytes型の場合しかありえないが、一応全型に対応するため変換
    str_path = str(database_path)
    is_memory = str_path == ":memory:" or "mode=memory" in str_path

    if is_memory:
        # インメモリの場合は作成を行う
        logger.debug("In-memory database is specified.")
        return (True, True)

    # ファイルの存在を確認
    db_path = Path(database_path)
    if not db_path.exists():
        # ファイルが存在しない場合は作成が必要
        logger.debug("Database file is not exists.")
        return (True, True)
    
    # ファイルが存在する場合は管理テーブルの存在を確認
    with sqlite3.connect(database_path) as conn:
        is_exist = is_exist_table_udam_status(conn)
    
    if not is_exist:
        # 管理テーブルが存在しない場合は作成が必要
        logger.debug("Database file is exists, but udam_status table is not exists.")
        return (False, True)
    
    logger.debug("Database file is exists, and udam_status table is exists.")
    return (False, False)

