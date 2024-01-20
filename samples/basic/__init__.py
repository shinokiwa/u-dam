from u_dam.sqlite3 import UdamParams

# U-DAMのデータベース設定パラメータ
UDAM_PARAMS = UdamParams(
    # 現在のデータベースバージョン
    # tablesパッケージを適用した時点のバージョンを設定する。
    # INT型のみ許容する。
    version=1,

    # 自動的にテーブルを作成する配下パッケージ名
    auto_initialize_package="tables",

    # テーブル作成のメソッド名
    create_table="create_table",

    # tablesパッケージのうち、自動的にテーブルを作成するモジュールのリスト
    # 記載順に作成される。
    auto_initialize_tables=[ 
        "users",
        "no_create_table", # create_tableメソッドが存在しないものは無視される
    ]
)