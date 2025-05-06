# app/services/answer_chat_service.py
# ChatRequest, ChatResponse, ChatMessage モデルはそのまま使用
from app.models.chat_models import ChatRequest, ChatResponse, ChatMessage
# generate_chat_response 関数をインポート
from app.services.ai_service import generate_chat_response
# List 型ヒントはそのまま使用
from typing import List

# このサービスが担当するAIへのシステム指示を定義
ANSWER_AND_WHY_MODE_SYSTEM_INSTRUCTION = (
    "ユーザーからの質問に対し、まず正確な答えを簡潔に回答してください。"
    "その回答に続いて、「さて、なぜその答えになるのか、あなたの考えを教えてください。」"
    "あるいはそれに類する、ユーザーに回答の根拠や推論プロセスを尋ねる形の質問を生成し、応答を締めくくってください。"
    "会話履歴を考慮して、自然な流れで応答してください。"
     # Geminiに指示として認識させるため、ユーザー発話の形式にするのがコツ
)

async def process_answer_and_why_request(request: ChatRequest) -> ChatResponse:
    """
    '答え+なぜ？'モードのチャットリクエストを処理する。
    """
    print("Service: Processing answer and why mode request...")

    try:
        # AIに渡す会話履歴リストを作成
        # ★ システム指示を最初のメッセージとして追加 ★
        history_for_ai: List[ChatMessage] = [
            ChatMessage(role="user", content=ANSWER_AND_WHY_MODE_SYSTEM_INSTRUCTION)
        ] + request.history # 元の履歴リストの後に追加

        # 1. AIサービスを呼び出し
        # 現在のユーザー質問と、システム指示を含む会話履歴リストを渡す
        ai_response_text = await generate_chat_response(
            current_message_content=request.question,
            history=history_for_ai # システム指示を含む履歴を渡す
        )

        # 2. AIからの応答を処理（ここでは単純にそのまま返す）
        processed_response = ai_response_text

        print("Service: Answer and why mode processing complete.")

        # 3. レスポンスモデルに格納して返す
        return ChatResponse(response=processed_response)

    except Exception as e:
        print(f"Service Error in answer and why mode: {e}")
        raise # API層でキャッチさせるため再Raise