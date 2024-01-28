"""
メイン処理 イニシャライズ
現状たんにスケルトンディレクトリをコピーするだけ。
"""
import os
import shutil
import sys
from pathlib import Path

def initialize(target_dir:str):
    """
    メイン処理

    指定したディレクトリにスケルトンディレクトリをコピーする。
    既にディレクトリが存在する場合はエラーとする。
    """
    # ディレクトリが存在する場合はエラー
    if os.path.exists(target_dir):
        print(f'Error: {target_dir} already exists.')
        sys.exit(1)

    # スケルトンディレクトリをコピー
    shutil.copytree(
        Path(__file__).parent / 'skelton',
        target_dir
    )


if __name__ == '__main__': # pragma: no cover
    if len(sys.argv) < 2:
        print('Usage: python -m udam.sqlite3.init <target_dir>')
        sys.exit(1)

    initialize(sys.argv[1])