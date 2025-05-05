# app/services/thinking_chat_service.py
from app.models.chat_models import ChatRequest, ChatResponse, ChatMessage
from app.services.ai_service import get_ai_response_from_model, build_ai_prompt
from typing import List

# このサービスが担当するAIへの指示を定義
THINKING_MODE_INSTRUCTION = (
    "あなたは直接的な答えを教えてはいけません。代わりに、その答えにたどり着くための思考プロセスや、"
    "どのようなキーワードで検索すれば情報が見つかるかを具体的にステップ形式で教えてください。"
)

async def process_thinking_request(request: ChatRequest) -> ChatResponse:
    """
    '考え方や調べ方'モードのチャットリクエストを処理する。
    """
    print("Service: Processing thinking mode request...")

    # 1. AIへのプロンプトを構築
    # 会話履歴も渡すが、このモードでは過去の質問の「考え方」を聞くケースは少ないかもしれない
    # 必要に応じて履歴の扱い方は調整
    prompt = build_ai_prompt(
        user_question=request.question,
        mode_instruction=THINKING_MODE_INSTRUCTION,
        history=request.history # 会話履歴も渡す
    )

    # 2. AIサービスを呼び出し
    ai_raw_response = await get_ai_response_from_model(
        prompt=prompt,
        history=request.history # AIモデルがメッセージリスト形式を要求する場合などに必要
    )

    # 3. AIからの応答を処理（ここでは単純にそのまま返す）
    # 必要であれば、AI応答の形式をチェックしたり加工したりする
    processed_response = ai_raw_response

    print("Service: Thinking mode processing complete.")

    # 4. レスポンスモデルに格納して返す
    return ChatResponse(response=processed_response)

# クラスベースにすることも検討可能 (例: 依存性注入などが必要になった場合)
# class ThinkingChatService:
#     def __init__(self, ai_client: AICallInterface): # AI連携部分をDIする例
#         self.ai_client = ai_client
#
#     async def process_request(self, request: ChatRequest) -> ChatResponse:
#         ... self.ai_client を使って AI 呼び出し ...