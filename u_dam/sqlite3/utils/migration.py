"""
マイグレーションスクリプトのリストを取得する
"""
import logging; logger = logging.getLogger(__name__)
from typing import Dict
import os
import re
import importlib.util
from importlib import import_module
import sqlite3
from pathlib import Path

from ..database.tables.status import (
    set_udam_status,
    UdamStatusKeys
)

def do_migration (conn:sqlite3.Connection, package_name:str, version_key:UdamStatusKeys, start_version:int):
    """
    マイグレーションを実行する
    """

    # パッケージ名からディレクトリを取得
    directory = Path(import_module(package_name).__file__).parent / 'versions'

    # マイグレーションスクリプトを取得
    migration_scripts = load_migration_scripts(directory)

    # マイグレーションスクリプトを実行
    run_migration_scripts(conn, migration_scripts, version_key, start_version)

# 正規表現だけテストするために、グローバル変数にしている
regexp = re.compile(r'^v(\d+)(_.*)?\.py$')

def load_migration_scripts(directory:Path):
    """
    マイグレーションスクリプトのリストを取得する
    """
    migration_scripts = []
    # ディレクトリ内のすべてのPythonファイルをリストアップ
    for f in os.listdir(directory):
        if f.endswith('.py'):
            matches = regexp.match(f)
            if matches is None:
                continue

            # ファイル名からバージョン番号を取得
            version = int(matches.group(1))

            migration_scripts.append({
                'version': version,
                'script_path': os.path.join(directory, f)
            })
    return migration_scripts

def run_migration_scripts (conn:sqlite3.Connection, migration_scripts:Dict, version_key:UdamStatusKeys, start_version:int):
    """
    マイグレーションスクリプトを実行する
    """
    for script in migration_scripts:
        version = script['version']
        script_path = script['script_path']
        if version <= start_version:
            # バージョンが開始バージョンよりも小さい場合はスキップ
            logger.debug(f"already migrated: {script_path}")
            continue

        # スクリプトを動的にインポートして実行
        spec = importlib.util.spec_from_file_location(f"migration_v{version}", script_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        # マイグレーションスクリプトを実行
        if hasattr(module, 'upgrade'):
            module.upgrade(conn)
            logger.debug(f"run migration script: {script_path}")
        else:
            logger.debug(f"migration function not found: {script_path}")

        set_udam_status(conn, version_key, str(version))
        conn.commit()

