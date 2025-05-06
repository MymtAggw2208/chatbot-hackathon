# app/services/ai_service.py
import os
import asyncio
import google.generativeai as genai
import google.generativeai.types as genai_types
# List と Optional は必要。Dict, Any を typing からインポート
from typing import List, Optional, Dict, Any
# ChatMessage モデルをインポート
from app.models.chat_models import ChatMessage

# .env ファイルから環境変数を読み込む (ローカル開発用)
from dotenv import load_dotenv
load_dotenv()

# 環境変数からGemini APIキーを取得
API_KEY = os.getenv("GEMINI_API_KEY")

# APIキーが設定されているか確認
if not API_KEY:
    raise ValueError("GEMINI_API_KEY environment variable not set.")

# Gemini API を設定
genai.configure(api_key=API_KEY)

# 使用するモデルを指定
MODEL_NAME = "gemini-2.0-flash"

# ChatMessage の role ('user', 'assistant') を Gemini API が期待する 'user', 'model' にマッピング
ROLE_MAPPING = {
    "user": "user",
    "assistant": "model", # Gemini API は 'model' ロールを使用します
}

async def generate_chat_response(
    current_message_content: str,
    history: List[ChatMessage]
) -> str:
    """
    Gemini API を使用してチャット応答を生成する。
    システム指示は history リストの最初のメッセージとして含めることを想定。
    履歴は辞書形式に変換して渡す。

    Args:
        current_message_content: ユーザーからの現在のメッセージ本文。
        history: 過去の会話履歴 (ChatMessage オブジェクトのリスト)。
                 システム指示を含める場合は、リストの最初の要素として
                 ChatMessage(role='user', content='指示内容') を含める。

    Returns:
        AIからの応答本文。

    Raises:
        Exception: API呼び出し中にエラーが発生した場合。
    """
    print("--- Calling Gemini AI Service ---")
    print(f"Current Message: {current_message_content[:50]}...")
    print(f"History Length: {len(history)}")
    print("-----------------------------")

    try:
        # 渡された history リストを Gemini API が受け付ける辞書形式のリストに変換
        gemini_history: List[Dict[str, Any]] = []
        for message in history:
            role = ROLE_MAPPING.get(message.role)
            if role:
                 gemini_history.append({
                     "role": role,
                     "parts": [{"text": message.content}] # テキストは parts リストの中の辞書に入れる形式
                 })
            else:
                 print(f"Warning: Unknown role in history: {message.role}. Skipping.")


        # Gemini モデルインスタンスを取得
        model = genai.GenerativeModel(MODEL_NAME)

        # チャットセッションを開始
        # 辞書形式のリストを history として渡します。
        chat_session = model.start_chat(history=gemini_history)

        # 現在のユーザーメッセージを送信し、応答を待つ
        # send_message_async は非同期なので await します
        response = await chat_session.send_message_async(current_message_content)

        # 応答からテキスト部分を抽出して返す
        if response.text:
             return response.text
        elif response.candidates:
             # text 属性がない場合でも候補があればそれを返すなど、柔軟に対応
             print(f"Warning: Response.text is empty, checking candidates.")
             if response.candidates[0].content.parts:
                 # 応答候補の最初のパートのテキストを返す
                 if isinstance(response.candidates[0].content.parts[0], genai_types.TextPart):
                     return response.candidates[0].content.parts[0].text
                 else:
                      # テキストパートでない場合（画像など）の考慮
                      print(f"Warning: First candidate part is not text: {type(response.candidates[0].content.parts[0])}")
                      return "AIからの応答がテキスト形式ではありませんでした。"
             else:
                 return "AIから有効な応答が得られませんでした（候補パートなし）。"
        else:
             print(f"Warning: AI response is empty or blocked. Response: {response}")
             if response.prompt_feedback and response.prompt_feedback.block_reason:
                  block_reason = response.prompt_feedback.block_reason
                  print(f"Response was blocked due to: {block_reason}")
                  if block_reason == genai_types.BlockedReason.SAFETY:
                      return "不適切な内容のため応答を生成できませんでした。"
                  else:
                      return "AIによる応答生成に問題が発生しました（理由不明）。"
             return "AIからの応答が得られませんでした。"


    except Exception as e:
        print(f"An error occurred during AI API call: {e}")
        raise Exception(f"AIサービスとの通信中にエラーが発生しました: {e}") # API層でキャッチされるように例外を再Raise