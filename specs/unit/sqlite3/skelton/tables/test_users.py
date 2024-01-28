"""
u_dam.sqlite3.skelton.tables.users のテスト
"""
import pytest
import sqlite3

from u_dam.sqlite3.skelton.tables.users import *

def test_create_table ():
    """
    スケルトンディレクトリは単にエラーがない程度でOK
    """
    conn = sqlite3.connect(':memory:')
    create_table(conn)
