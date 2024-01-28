"""
u_dam.sqlite3.init のテスト
"""
import pytest
from pytest_mock import MockerFixture

from u_dam.sqlite3.init import *

def test_initialize (mocker:MockerFixture):
    """
    init

    it:
        - スケルトンディレクトリをコピーする。
        - 既にディレクトリが存在する場合はエラーとする。
    """

    mock_exists = mocker.patch('os.path.exists')
    mock_copytree = mocker.patch('shutil.copytree')

    # ディレクトリが存在する場合はエラー
    mock_exists.return_value = True
    with pytest.raises(SystemExit):
        initialize('target_dir')

    # スケルトンディレクトリをコピー
    mock_exists.return_value = False
    initialize('target_dir')

    assert mock_copytree.call_count == 1
    assert str(mock_copytree.call_args[0][0]).endswith('skelton')
    assert mock_copytree.call_args[0][1] == 'target_dir'