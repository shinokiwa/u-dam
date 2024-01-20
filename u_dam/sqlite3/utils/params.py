"""
UDAM_PARAMSの設定クラス
"""
from typing import List
from dataclasses import dataclass
from importlib import import_module

@dataclass
class UdamParams:
    version:int = 1
    auto_initialize_package:str = None
    create_table:str = "create_table"
    auto_initialize_tables:List[str] = None

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

