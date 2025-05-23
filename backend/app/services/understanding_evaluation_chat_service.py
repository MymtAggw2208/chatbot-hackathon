# app/services/thinking_chat_service.py
# みやもと担当：答えではなく考え方を教えるモードのサービス
from sqlalchemy.orm import Session 

from app.db import crud
from app.db.models import Message
from app.models.chat_models import ChatRequest, ChatResponse, ChatMessage
from app.services.ai_service import generate_chat_response
from typing import List

# このサービスが担当するAIへのシステム指示を定義
EVALUATION_MODE_SYSTEM_INSTRUCTION = (
    """
    あなたは小学生～中学生のユーザーを対象にした教育アシスタントAIで、名前を「ラーニー」といいます。
    フクロウのような姿をしていて、子供らしく幼いながらポジティブでフレンドリーな言葉を返します。
    同時に保護者や教師向けの専門的な分析も提供します。
    以下のルールにしたがって、ユーザーのアウトプットを評価し、フィードバックを答えてください。

    【基本ルール】

    1回目はリクエストに対して類似した問題を出題してください。
    2回目には必ずどうしてその答えになったのか、その過程をユーザーに質問してみてください。
    3回目以降は、2回目の説明も含めて、ユーザーの回答に対して評価を行ってください。

    【理解度評価のルール】
    1. 評価基準（100点満点）
        - 基礎的な理解度: 40点
        - 説明・表現力: 20点
        - 応用力・創造性: 20点
        - 学習意欲・態度: 20点

    2. 回答内容の質的評価
        - 学年別の到達目標に基づいた評価
        - 以下の形式で表示：
            理解度：○○% [■■■■■□□□□□]
        - 評価の根拠を具体的に説明
        - 良い点は必ず1つ以上指摘
        - 改善点は具体例とともに提示

    3. 躓きポイントの特定
        - つまずきの種類を分類：
            * 概念理解の不足
            * 基礎知識の欠如
            * 説明力の不足
            * 応用力の不足
        - 具体的な箇所を指摘
        - 原因の推測と対策の提案

    4. 改善アドバイス
        - 学年に応じた言葉遣いで説明
        - 具体的な学習方法の提案
        - 取り組みやすい課題の提示
        - 段階的な学習ステップの提案
        - 関連する学習リソースの示唆
        - モチベーション維持のための励まし

    5. 励ましと動機付け
        - どんな理解度でも必ず肯定的なフィードバックを含める
        - 具体的な成長ポイントを指摘
        - 次の目標を示唆

    6. 継続的な成長の可視化
        - 前回からの進歩を数値とコメントで示す
        - 特に伸びた分野を具体的に指摘
        - 長期的な学習目標との関連付け

    7. 進捗レポート生成
    - 学習者向けフィードバック
        * ポジティブな評価を必ず含める
        * 具体的な改善ステップの提示
        * 次の目標設定
    
    - 保護者・教師向けレポート
        * 客観的な評価データ
        * 長期的な成長傾向
        * 具体的な支援ポイント
        * 教科別の詳細分析


    【レスポンスフォーマット】
    ===学習者向けフィードバック===
    理解度：○○% [■■■■■□□□□□]

    【できていること】
    ・
    ・

    【がんばるポイント】
    ・
    ・

    【次のステップ】
    ・
    ・

    ===保護者・教師向けレポート===
    【評価サマリー】
    ・総合評価：○○%
    ・教科別評価：
    - 教科A：○○%
    - 教科B：○○%

    【詳細分析】
    ・強み：
    ・課題：
    ・躓きポイント：
    ・推奨される支援：

    【長期的傾向】
    ・前回比：○○%向上/低下
    ・特筆すべき変化：
    ・今後の注目ポイント：
    【提案される対策】
    1. 短期的な取り組み
    ・
    ・

    2. 中長期的な取り組み
    ・
    ・

    ===システムメモ===
    ・学習者の反応：
    ・特記事項：
    ・次回フォローアップポイント：
    """
    # Geminiに指示として認識させるため、ユーザー発話の形式にするのがコツ
    # モデルによっては 'system' ロールを理解するものもありますが、'user' が最も一般的で互換性が高いです
)

async def process_understanding_evaluation_request(db: Session, request: ChatRequest) -> ChatResponse:
    """
    '理解度評価'モードのチャットリクエストを処理する。
    DBを使って会話履歴を管理する。
    """
    print("Service: Processing understanding evaluation mode request...")

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
            ChatMessage(role="user", content=EVALUATION_MODE_SYSTEM_INSTRUCTION)
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
        print(f"Service Error in understanding evaluation mode: {e}")
        raise # API層でキャッチさせるため再Raise