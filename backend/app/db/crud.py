# app/db/crud.py
from sqlalchemy.orm import Session
from .models import Conversation, Message # 定義したモデルをインポート
from app.models.chat_models import ChatMessage # アプリケーション層のモデルも必要に応じて使用
from typing import List, Optional

# 会話を作成
def create_conversation(db: Session) -> Conversation:
    """新しい会話を作成し、DBに保存する"""
    db_conversation = Conversation()
    db.add(db_conversation) # セッションに追加
    db.commit() # DBに保存
    db.refresh(db_conversation) # DBの状態を反映
    return db_conversation

# メッセージを作成し、会話に追加
def create_message(db: Session, conversation_id: int, role: str, content: str) -> Message:
    """指定した会話に新しいメッセージを追加する"""
    db_message = Message(conversation_id=conversation_id, role=role, content=content)
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    return db_message

# 会話履歴を取得
def get_conversation_history(db: Session, conversation_id: int) -> List[Message]:
    """指定した会話IDのメッセージ履歴を作成日時順に取得する"""
    # Conversation モデルを使ってリレーションシップからメッセージを取得することも可能
    # conversation = db.query(Conversation).filter(Conversation.id == conversation_id).first()
    # if conversation:
    #     # リレーションシップがロードされている場合（lazy設定による）
    #     return sorted(conversation.messages, key=lambda msg: msg.created_at)

    # シンプルにMessageテーブルから取得
    messages = db.query(Message).filter(Message.conversation_id == conversation_id).order_by(Message.created_at).all()
    return messages

# Message モデルのリストを ChatMessage モデルのリストに変換するヘルパー
def messages_to_chat_messages(messages: List[Message]) -> List[ChatMessage]:
    """DBのMessageオブジェクトのリストを、アプリケーションのChatMessageオブジェクトのリストに変換する"""
    return [ChatMessage(role=msg.role, content=msg.content) for msg in messages]

# 他にも、特定の会話を取得する関数や、会話を削除する関数などをここに追加できます
# def get_conversation(db: Session, conversation_id: int) -> Optional[Conversation]:
#     return db.query(Conversation).filter(Conversation.id == conversation_id).first()

# def delete_conversation(db: Session, conversation_id: int):
#     db.query(Conversation).filter(Conversation.id == conversation_id).delete()
#     db.commit()