"""
u_dam.sqlite3.utils.params のテスト
"""
import pytest

from u_dam.sqlite3.utils.params import *

def test_get_udam_params ():
    """
    get_udam_params

    it:
        - UDAM_PARAMSを取得する。
        - UDAM_PARAMSがUdamParamsでない場合は、例外を発生する。
    """
    params = get_udam_params('samples.p001_basic')
    assert isinstance(params, UdamParams)
    assert params.initial_version == 1

def test_get_udam_params_error ():
    """
    get_udam_params

    error:
        - UDAM_PARAMSがUdamParamsでない場合は、例外を発生する。
    """

    # パッケージが存在しない
    with pytest.raises(Exception) as e:
        get_udam_params("not_exists")
    
    assert str(e.value) == "No package named 'not_exists'"

    # UDAM_PARAMSが存在しない
    with pytest.raises(Exception) as e:
        get_udam_params("specs.database.error_no_params")
    
    assert str(e.value) == "UDAM_PARAMS is not defined in specs.database.error_no_params"

    # UDAM_PARAMSがUdamParamsでない
    with pytest.raises(Exception) as e:
        get_udam_params("specs.database.error_invalid_params")
    
    assert str(e.value) == "UDAM_PARAMS is not UdamParams in specs.database.error_invalid_params"


    