# app/services/answer_chat_service.py
from app.models.chat_models import ChatRequest, ChatResponse, ChatMessage
from app.services.ai_service import get_ai_response_from_model, build_ai_prompt
from typing import List

# このサービスが担当するAIへの指示を定義
ANSWER_AND_WHY_MODE_INSTRUCTION = (
    "質問にまず回答してください。その上で、なぜその回答になるのか、"
    "ユーザーに理由や根拠を尋ねるような質問を続けてください。"
)

async def process_answer_and_why_request(request: ChatRequest) -> ChatResponse:
    """
    '答え+なぜ？'モードのチャットリクエストを処理する。
    会話履歴を使ってAIに文脈を提供することが重要。
    """
    print("Service: Processing answer and why mode request...")

    # 1. AIへのプロンプトを構築
    # このモードでは、AIが「答え」と「なぜ？」という質問を生成するために
    # 現在の質問だけでなく、過去の会話履歴も重要な情報となります。
    prompt = build_ai_prompt(
        user_question=request.question,
        mode_instruction=ANSWER_AND_WHY_MODE_INSTRUCTION,
        history=request.history # 会話履歴必須
    )

    # 2. AIサービスを呼び出し
    # AIは、返答の中に「答え」と「なぜ？」の質問の両方を含めるように期待されます。
    ai_raw_response = await get_ai_response_from_model(
        prompt=prompt,
        history=request.history # AIモデルがメッセージリスト形式を要求する場合などに必要
    )

    # 3. AIからの応答を処理（ここでは単純にそのまま返す）
    # 実際には、応答が期待通りの形式（答えと質問が含まれているかなど）になっているか
    # チェックしたり、パースしたりする必要があるかもしれません。
    processed_response = ai_raw_response

    print("Service: Answer and why mode processing complete.")

    # 4. レスポンスモデルに格納して返す
    return ChatResponse(response=processed_response)

# クラスベースにすることも検討可能 (例: 会話履歴の永続化などが必要になった場合)
# class AnswerAndWhyChatService:
#     def __init__(self, ai_client: AICallInterface, history_repo: HistoryRepository): # AI連携と履歴管理をDIする例
#         self.ai_client = ai_client
#         self.history_repo = history_repo
#
#     async def process_request(self, request: ChatRequest) -> ChatResponse:
#         # history_repo を使って履歴を取得/保存
#         ...