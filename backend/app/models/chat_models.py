# app/models/chat_models.py
from pydantic import BaseModel
from typing import List, Dict, Any

# 会話の1ターンを表すモデル
class ChatMessage(BaseModel):
    role: str  # メッセージの送信者 ("user" または "assistant" など)
    content: str # メッセージ本文

# チャットリクエストのモデル
class ChatRequest(BaseModel):
    question: str # ユーザーからの現在の質問
    history: List[ChatMessage] = [] # 過去の会話履歴 (オプション、デフォルトは空リスト)

# チャットレスポンスのモデル
class ChatResponse(BaseModel):
    response: str # AIからの応答本文
    # 今後の拡張として、応答の種類や追加情報などをここに追加可能
    # type: str = "text" # 例: "text", "steps", "answer_why"
    # metadata: Dict[str, Any] = {}