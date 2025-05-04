# app/main.py
from fastapi import FastAPI

# FastAPIアプリケーションインスタンスを作成
app = FastAPI()

# ルート ("/") へのGETリクエストに対するエンドポイントを定義
@app.get("/")
def read_root():
    return {"Hello": "World"}

# 例: /items/{item_id} のようなパスパラメータを持つエンドポイント
@app.get("/items/{item_id}")
def read_item(item_id: int, q: str | None = None): # 型ヒントを付けることで自動的に検証されます
    return {"item_id": item_id, "q": q}