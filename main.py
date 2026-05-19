from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database import Base, engine, check_db_connection
from routers import threads, posts


@asynccontextmanager
async def lifespan(app: FastAPI):
    # 起動時: DB 接続確認 → テーブル自動作成
    check_db_connection()
    Base.metadata.create_all(bind=engine)
    yield
    # 終了時: 必要に応じてここにクリーンアップ処理を追加


app = FastAPI(title="Anonymous BBS API", version="0.1.0", lifespan=lifespan)

origins = [
    "http://localhost:5173",  # ローカル開発
    "https://anonymous-bbs.vercel.app",  # Vercel 本番
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(threads.router, prefix="/api")
app.include_router(posts.router, prefix="/api")


@app.get("/health")
def health():
    return {"status": "ok"}
