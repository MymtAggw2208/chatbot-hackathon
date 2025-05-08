# app/services/thinking_chat_service.py
from sqlalchemy.orm import Session 

from app.db import crud
from app.db.models import Message
from app.models.chat_models import ChatRequest, ChatResponse, ChatMessage
from app.services.ai_service import generate_chat_response
from typing import List

# このサービスが担当するAIへのシステム指示を定義
THINKING_MODE_SYSTEM_INSTRUCTION = (
    "あなたはユーザーからの質問に対し、直接的な答えを教えず、"
    "その答えにたどり着くための思考プロセスや、効果的な調べ方、検索キーワードなどを、"
    "具体的かつ分かりやすいステップ形式で回答してください。"
    "ユーザーの学習を助けることに焦点を当ててください。"
    # Geminiに指示として認識させるため、ユーザー発話の形式にするのがコツ
    # モデルによっては 'system' ロールを理解するものもありますが、'user' が最も一般的で互換性が高いです
)

async def process_thinking_request(db: Session, request: ChatRequest) -> ChatResponse:
    """
    '考え方や調べ方'モードのチャットリクエストを処理する。
    DBを使って会話履歴を管理する。
    """
    print("Service: Processing thinking mode request...")

    try:
        conversation_id = request.conversation_id
        current_question_text = request.question

        # 1. 会話の特定または新規作成
        if conversation_id is None:
            # 新しい会話の場合、DBに会話エントリを作成
            conversation = crud.create_conversation(db)
            conversation_id = conversation.id
            print(f"Service: Created new conversation with ID: {conversation_id}")
        else:
             # 既存の会話の場合、IDが存在するか確認するなど堅牢化も必要
             print(f"Service: Using existing conversation with ID: {conversation_id}")
             # ここで、そのconversation_idが本当に存在するかDBで確認する処理を入れるのが望ましい

        # 2. DBから会話履歴を取得
        db_messages = crud.get_conversation_history(db, conversation_id)

        # DBから取得した履歴を、AIサービスが期待する ChatMessage のリスト形式に変換
        history_for_ai: List[ChatMessage] = crud.messages_to_chat_messages(db_messages)

        # システム指示をAIに渡す履歴リストの先頭に追加
        history_for_ai_with_instruction: List[ChatMessage] = [
            ChatMessage(role="user", content=THINKING_MODE_SYSTEM_INSTRUCTION)
        ] + history_for_ai

        # 3. AIサービスを呼び出し
        # 現在のユーザー質問と、システム指示+DB履歴を含む会話履歴リストを渡す
        ai_response_text = await generate_chat_response(
            current_message_content=current_question_text,
            history=history_for_ai_with_instruction # システム指示+DB履歴を渡す
        )

        # 4. ユーザーの質問とAIの応答をDBに保存
        crud.create_message(db, conversation_id, "user", current_question_text)
        crud.create_message(db, conversation_id, "assistant", ai_response_text) # AIのロールは 'assistant' で保存

        # 5. レスポンスモデルに格納して返す
        return ChatResponse(
            response=ai_response_text,
            conversation_id=conversation_id # 新規作成/既存問わず会話IDを返す
        )

    except Exception as e:
        print(f"Service Error in thinking mode: {e}")
        raise # API層でキャッチさせるため再Raise