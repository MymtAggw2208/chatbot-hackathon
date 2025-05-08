# app/db/models.py
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func # 現在時刻取得用
from .database import Base # database.py で定義したBaseをインポート

# 会話テーブル
class Conversation(Base):
    __tablename__ = "conversations" # テーブル名

    id = Column(Integer, primary_key=True, index=True) # 会話ID (主キー)
    created_at = Column(DateTime(timezone=True), server_default=func.now()) # 作成日時

    # この会話に属するメッセージとのリレーションシップを定義
    # 'lazy="joined"' で会話取得時にメッセージも一緒に取得（オプション）
    # 'cascade="all, delete-orphan"' で会話削除時にメッセージも削除
    messages = relationship("Message", back_populates="conversation", cascade="all, delete-orphan")

# メッセージテーブル
class Message(Base):
    __tablename__ = "messages" # テーブル名

    id = Column(Integer, primary_key=True, index=True) # メッセージID (主キー)
    conversation_id = Column(Integer, ForeignKey("conversations.id"), index=True) # 会話ID (外部キー)
    role = Column(String, index=True) # 役割 (user, assistant/model など)
    content = Column(Text) # メッセージ本文 (長いテキスト用)
    created_at = Column(DateTime(timezone=True), server_default=func.now()) # 作成日時

    # 属している会話とのリレーションシップを定義
    conversation = relationship("Conversation", back_populates="messages")