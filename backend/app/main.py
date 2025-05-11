# app/main.py
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from app.api import chat_routes # APIルーターをインポート
# 他に必要な初期化処理があればインポート (DB接続など)

# (オプション) アプリケーション起動/終了時の処理を定義
# from contextlib import asynccontextmanager
#
# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     # アプリケーション起動時に実行される処理
#     print("Backend startup...")
#     # 例: データベース接続プールの初期化
#     # await database.connect()
#     yield
#     # アプリケーション終了時に実行される処理
#     print("Backend shutdown...")
#     # 例: データベース接続プールのクローズ
#     # await database.disconnect()

# FastAPI アプリケーションインスタンスを作成
# タイトルなどを設定すると、自動生成されるドキュメントが見やすくなります (/docs)
app = FastAPI(
    title="My Chatbot Backend",
    version="0.1.0",
    description="Backend API for the AI Chatbot",
    # lifespan=lifespan # 起動/終了時処理を使う場合
)

# APIルーターをアプリケーションに含める
# chat_routes.router を /chat というプレフィックスで登録します
# これにより、chat_routes.py で定義した /thinking は /chat/thinking でアクセス可能になります
app.include_router(chat_routes.router, prefix="/chat", tags=["Chat"]) # tagsはドキュメント用

# ルートパス "/" へのアクセスがあった場合の処理 (オプション)
# よくAPIドキュメントへのリダイレクトに使われます
@app.get("/", include_in_schema=False) # APIドキュメントには表示しない
def read_root():
    return RedirectResponse(url="/docs") # /docs (Swagger UI) へリダイレクト

# --- その他、アプリケーション全体の設定やミドルウェアなどをここに追加 ---
# 例: CORS設定
from fastapi.middleware.cors import CORSMiddleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# ------------------------------------------------------------------

# 注意: この main.py ファイル自体を直接実行することは通常ありません
# 実行は uvicorn コマンドで行います: uvicorn app.main:app --reload