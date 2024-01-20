"""
UDAM_PARAMSの設定クラス
"""
from typing import List
from dataclasses import dataclass

@dataclass
class UdamParams:
    version:int = 1
    auto_initialize_package:str = None
    create_table:str = "create_table"
    auto_initialize_tables:List[str] = None
