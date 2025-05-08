# app/db/database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os # 環境変数を読むため

# .env ファイルから環境変数を読み込む (ローカル開発用)
from dotenv import load_dotenv
load_dotenv()

# データベースURLを環境変数から取得
# 環境変数がない場合は SQLite のデフォルトパスを使用
# 例: DATABASE_URL="postgresql://user:password@host:port/dbname"
# 例: DATABASE_URL="sqlite:///./sql_app.db" # 相対パス
# 例: DATABASE_URL="sqlite:////absolute/path/to/sql_app.db" # 絶対パス
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./test.db")

# SQLite を使う場合、複数スレッドからのアクセスを許可する設定が必要
# 他のDB (PostgreSQLなど) の場合は不要です
connect_args = {}
if SQLALCHEMY_DATABASE_URL.startswith("sqlite"):
    connect_args["check_same_thread"] = False

# SQLAlchemy エンジンを作成
# echo=True にすると、実行されるSQLログが表示されてデバッグに便利です（本番ではFalse推奨）
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args=connect_args,
    echo=False # デバッグ時はTrueに
)

# データベースセッションを作成するためのファクトリ
# autocommit=False, autoflush=False で、明示的にコミットするまで変更を保留
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# ORMモデルのベースクラス
# これを継承してテーブルクラスを定義します
Base = declarative_base()

# FastAPIのDependsで使用するDBセッション取得の依存性注入ヘルパー
def get_db():
    """
    リクエストごとにデータベースセッションを作成し、処理後にクローズする。
    FastAPIのDependsとして使用。
    """
    db = SessionLocal()
    try:
        yield db # セッションを呼び出し元に渡す
    finally:
        db.close() # リクエスト処理後にセッションをクローズ