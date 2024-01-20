# バージョン履歴管理モジュール

## 概要

データベースのバージョン履歴を管理するモジュールです。

## 使い方

### マイグレーションファイルの作成

ファイル名は、以下のルールで作成してください。

```
v{バージョン番号}_{履歴名称}.py
```

vとバージョン番号のみ必須で、履歴名称は任意です。<br>
バージョン番号が現在よりも大きいモジュールが、バージョン番号順に実行されます。<br>
モジュールは以下のように作成します。

```python
import sqlite3

def upgrade (conn:sqlite3.Connection) -> None:
    """
    バージョンアップ処理
    """
    conn.executescript((
        "ALTER TABLE users ADD COLUMN age INTEGER;"
    ))

def downgrade (conn:sqlite3.Connection) -> None:
    """
    バージョンダウン処理
    """
    conn.executescript((
        "ALTER TABLE users DROP COLUMN age;"
    ))
```

`downgrade`は、`upgrade`の逆の処理を行うようにしてください。<br>
必要がない場合は定義しなくても構いません。