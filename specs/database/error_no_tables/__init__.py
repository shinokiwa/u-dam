"""
指定されたテーブルが存在しない場合のテスト
ついでにauto_initialize_tablesが空の時のテストも行う。
"""
from u_dam.sqlite3 import UdamParams


UDAM_PARAMS = UdamParams(
    # 現在のデータベースバージョン
    # INT型のみ。
    initial_version=2,

    # 自動的にテーブルを作成する配下パッケージ名
    auto_initialize_package=None,

    # テーブル作成のメソッド名
    create_table="create_table",

    # tablesパッケージのうち、自動的にテーブルを作成するモジュールのリスト
    # 記載順に作成される。
    auto_initialize_tables=[ 
        "status",
    ]
)