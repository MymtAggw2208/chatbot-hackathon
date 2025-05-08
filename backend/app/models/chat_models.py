# app/models/chat_models.py
from pydantic import BaseModel
from typing import List, Dict, Any, Optional # Optional をインポート

# 会話の1ターンを表すモデル
class ChatMessage(BaseModel):
    role: str
    content: str

# チャットリクエストのモデル
class ChatRequest(BaseModel):
    question: str
    history: List[ChatMessage] = []
    # 会話IDを追加 - 新しい会話の場合は None を渡すことを想定
    conversation_id: Optional[int] = None

# チャットレスポンスのモデル
class ChatResponse(BaseModel):
    response: str
    # 会話IDを追加 - 次回のリクエストで使えるように返す
    conversation_id: int