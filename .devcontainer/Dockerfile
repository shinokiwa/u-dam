# Docker使うアプリではないので、これは開発環境のためのもの。

# 基本イメージとしてPythonの公式イメージを使用
FROM python:3.10

# 必要なパッケージをインストール
RUN apt-get update && apt-get install -y \
    locales \
    sqlite3 \
    && rm -rf /var/lib/apt/lists/*

# ロケールを設定
RUN locale-gen ja_JP.UTF-8

# 作業ディレクトリを設定
WORKDIR /workspace

# さしあたってsetuptoolsをインストール
RUN pip install --upgrade pip && \
    pip install setuptools

# ソースコピー
COPY ./ /workspace/

# pipインストール
RUN pip install .[dev]

#### 環境変数の設定 ####
ENV PYTHONPATH=/workspace

CMD ["tail", "-f", "/dev/null"]