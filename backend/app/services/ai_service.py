# app/services/ai_service.py
from app.models.chat_models import ChatMessage
from typing import List

# ここに実際のAIモデルとの通信処理を書きます
# (例: OpenAI API, Gemini API, ローカルモデルの呼び出しなど)

async def get_ai_response_from_model(prompt: str, history: List[ChatMessage]) -> str:
    """
    AIモデルにプロンプトと履歴を送信し、応答を取得する（モック）。

    実際の実装では、ここにAPIキーの設定、非同期HTTPリクエスト、
    エラーハンドリングなどのロジックが入ります。
    """
    print("--- Calling Mock AI Service ---")
    print(f"Prompt:\n{prompt}")
    print(f"History: {history}")
    print("-----------------------------")

    # !!! 実際のAIモデル呼び出しに置き換える !!!
    # 例:
    # import openai
    # messages = [{"role": msg.role, "content": msg.content} for msg in history]
    # messages.append({"role": "user", "content": prompt}) # プロンプトを最後のメッセージとして追加
    # response = await openai.ChatCompletion.acreate(
    #     model="gpt-4o-mini", # 利用するモデル
    #     messages=messages
    # )
    # return response.choices[0].message.content

    # これはあくまでモックの応答です
    # プロンプトの内容に応じて、それっぽいダミー応答を返します（非常に単純な例）
    if "考え方や調べ方を教えて" in prompt:
        mock_response = (
            f"（これはモック応答です - 考え方モード）\n\n"
            f"お尋ねの件について、答えそのものではなく、その考え方や調べ方をご案内します。\n"
            f"1. 問題の核心を捉えるキーワードを特定します。\n"
            f"2. 信頼できる情報源（書籍、論文、公式ドキュメントなど）を探します。\n"
            f"3. 特定したキーワードと情報源を使って調査を行います。\n"
            f"4. 複数の情報を比較検討し、自分なりの理解を深めます。"
        )
    elif "なぜその回答になるのか" in prompt:
         mock_response = (
            f"（これはモック応答です - 答え+なぜ？モード）\n\n"
            f"ご質問の件に対する答えは「モック回答」です。\n\n"
            f"さて、なぜこの答えが正しいと考えられるか、あなたの推論を聞かせてください。"
        )
    else:
        mock_response = f"（これはモック応答です）\n\n「{prompt[:50]}...」に対する一般的な応答です。"


    import asyncio
    await asyncio.sleep(0.1) # API呼び出しの待機を模倣

    return mock_response

# プロンプトを構築する関数（サービス層から呼び出される）
def build_ai_prompt(user_question: str, mode_instruction: str, history: List[ChatMessage]) -> str:
    """
    AIモデルに送るためのプロンプト文字列を構築する。
    会話履歴を含めたり、特定の指示（mode_instruction）を追加したりする。
    """
    # AIモデルが会話履歴をどのような形式で受け取るかによって、ここは大きく変わります。
    # 例えば、OpenAIやGeminiのAPIは messages=[...] のリスト形式を直接受け取ることが多いです。
    # この例では、履歴と現在の質問・指示を全て一つの文字列に詰め込む単純な形式とします。

    prompt_parts = []

    # 会話履歴をプロンプトに含める（モデルが履歴対応している場合）
    # 実際のAPIでは messages=[...] リスト形式で渡すことが多い
    # if history:
    #     prompt_parts.append("--- 会話履歴 ---")
    #     for msg in history:
    #         prompt_parts.append(f"{msg.role}: {msg.content}")
    #     prompt_parts.append("--- ここまで履歴 ---")

    # 現在のユーザーの質問
    prompt_parts.append(f"ユーザーからの質問：『{user_question}』")

    # モードに応じたAIへの指示
    if mode_instruction:
        prompt_parts.append(f"指示：{mode_instruction}")

    # 全体を結合してプロンプト文字列とする
    prompt = "\n".join(prompt_parts)

    return prompt