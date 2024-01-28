from u_dam.sqlite3 import UdamParams

# U-DAMのデータベース設定パラメータ
UDAM_PARAMS = UdamParams(
    # 現在tablesで作成されるテーブル群のバージョン
    # tablesパッケージを適用した時点のバージョンを設定する。
    # 整数値のみ。
    initial_version=1,

    # 自動的にバージョンアップする際の最大バージョン番号。
    # Noneの場合は可能な限りバージョンアップする。
    # 可能なら指定した方が高パフォーマンスになる。
    max_version=1,

    # 自動的にテーブルを作成する配下パッケージ名
    auto_initialize_package="tables",

    # テーブル作成のメソッド名
    create_table="create_table",

    # tablesパッケージのうち、自動的にテーブルを作成するモジュールのリスト
    # 記載順に作成される。
    auto_initialize_tables=[ 
        "users",
    ]
)