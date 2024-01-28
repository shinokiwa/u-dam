"""
UDAM_PARAMSの設定クラス
"""
from typing import List
from dataclasses import dataclass
from importlib import import_module

@dataclass
class UdamParams:
    initial_version:int
    """
    auto_initialize_packageで指定されたパッケージのバージョン番号。
    """

    auto_initialize_tables:List[str]
    """
    自動的にテーブルを作成するパッケージのリスト。
    """
    
    max_version:int = None
    """
    自動的にバージョンアップする場合の最大バージョン番号。
    Noneの場合は可能な限りバージョンアップする。
    """

    auto_initialize_package:str = "tables"
    """
    自動的にテーブルを作成するパッケージ名。
    """

    create_table:str = "create_table"

def get_udam_params (package_name:str) -> UdamParams:
    """
    パッケージのUDAM_PARAMSを取得する。

    Args:
        package_name: パッケージ名
    
    Returns:
        UdamParams

    Raises:
        Exception: パッケージが存在しない
        Exception: UDAM_PARAMSが存在しない
        Exception: UDAM_PARAMSがUdamParamsでない
    """
    try:
        package = import_module(package_name)
    except ModuleNotFoundError as e:
        raise Exception(f"No package named '{package_name}'") from e

    if not hasattr(package, 'UDAM_PARAMS'):
        raise Exception(f"UDAM_PARAMS is not defined in {package_name}")
    
    params = package.UDAM_PARAMS
    if not isinstance(params, UdamParams):
        raise Exception(f"UDAM_PARAMS is not UdamParams in {package_name}")
    
    return params

