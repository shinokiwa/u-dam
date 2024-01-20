"""
頻出する型を定義する
"""
from typing import Union
from os import PathLike
from pathlib import Path

StrOrBytesOrPath = Union[str, bytes, PathLike, Path]