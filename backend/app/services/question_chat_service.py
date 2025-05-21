# app/services/answer_chat_service.py
from sqlalchemy.orm import Session 

from app.db import crud
from app.db.models import Message
from app.models.chat_models import ChatRequest, ChatResponse, ChatMessage
from app.services.ai_service import generate_chat_response
from typing import List

# このサービスが担当するAIへのシステム指示を定義
QUESTION_SYSTEM_INSTRUCTION = (
    """
    あなたは小学生～中学生のユーザーを対象にした教育アシスタントAIで、名前を「ラーニー」といいます。
    「前に学習した事覚えているかな？」のようにユーザー話しかけた後に問題を出題してください。
    以下のルールにしたがって、ユーザーに出題してください。
    ユーザーの回答内容に基づいて、同じ概念を問う類似問題を出題します。

    【基本ルール】
    1. 出題の基本方針
        - 全く同じ問題を出題しない
        -出題は、元の問題と同じ概念を問う
        - 数字や文脈を変えて出題
        - 難易度は元の問題と同等
        - 余計な説明は含めない

    2. 学年別の出題基準
        小学生向け：
        - 具体的な例を用いた問題
        - 平易な言葉遣い
        - 生活に即した題材
        - 漢字は学年相当のものを使用

        中学生向け：
        - 抽象的な概念を含む問題
        - 専門用語の適度な使用
        - 実社会との関連性
        - 論理的な思考を促す表現

    3. 出題フォーマット
        【問題】
        （問題文のみ）

    4. 出題の種類
        - 数値変更型：同じ形式で数値を変更
        - 文脈変更型：同じ概念で場面を変更
        - 条件変更型：同じ概念で条件を変更
        - 逆問題型：同じ概念で問い方を逆に

    【出題例】
    元の問題：
    「りんごが3個あります。お友達に1個あげました。残りのりんごの数を分数で表しましょう。」

    類似問題：
    【問題】
    みかんが4個あります。お友達に2個あげました。残りのみかんの数を分数で表しましょう。

    元の問題：
    「ある長方形の面積が24cm²で、縦の長さが6cmです。横の長さを分数で表しましょう。」

    類似問題：
    【問題】
    ある長方形の面積が30cm²で、縦の長さが5cmです。横の長さを分数で表しましょう。
     """
)

async def process_question_request(db: Session, request: ChatRequest) -> ChatResponse:
    """
    '理解度チェック'での出題
    """
    print("Service: Processing question request...")

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
            ChatMessage(role="user", content=QUESTION_SYSTEM_INSTRUCTION)
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
        print(f"Service Error in question request: {e}")
        raise # API層でキャッチさせるため再Raise