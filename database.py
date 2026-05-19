from sqlalchemy import create_engine, text
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from sqlalchemy.exc import OperationalError
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./bbs.db")

_is_sqlite = DATABASE_URL.startswith("sqlite")

if _is_sqlite:
    # SQLite: スレッドチェックを無効化（FastAPI の非同期処理対応）
    engine = create_engine(
        DATABASE_URL,
        connect_args={"check_same_thread": False},
    )
else:
    # PostgreSQL: コネクションプールを明示的に設定
    engine = create_engine(
        DATABASE_URL,
        pool_size=5,          # 常時維持するコネクション数
        max_overflow=10,      # pool_size を超えた場合の最大追加数
        pool_pre_ping=True,   # 接続前に死活確認（切断済みコネクションの自動回復）
    )

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    pass


def check_db_connection() -> None:
    """起動時に DB への接続を確認する。失敗した場合は例外を送出する。"""
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
    except OperationalError as e:
        raise RuntimeError(f"データベースへの接続に失敗しました: {e}") from e


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
