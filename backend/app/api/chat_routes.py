# app/api/chat_routes.py
from fastapi import APIRouter, Depends, HTTPException, status 
from sqlalchemy.orm import Session
from app.models.chat_models import ChatRequest, ChatResponse
# サービス層のモジュールをインポート
from app.services import thinking_chat_service, answer_chat_service, understanding_evaluation_chat_service, question_chat_service
# database.py から get_db 依存性注入ヘルパーをインポート
from app.db.database import get_db


# APIRouter インスタンスを作成
# このルーター内の全てのエンドポイントは、main.py で設定された prefix (例: /chat) の下に配置されます。
router = APIRouter()

@router.post("/thinking",
             response_model=ChatResponse, # 返すレスポンスの形式を指定 (自動で検証・整形)
             status_code=status.HTTP_200_OK, # 成功時のステータスコード
             summary="考え方や調べ方を回答するチャット機能" # 自動生成ドキュメント用
            )
async def chat_thinking_endpoint(request: ChatRequest, db: Session = Depends(get_db)):
    """
    **考え方や調べ方モード**のチャットリクエストを受け付けます。

    - **question**: ユーザーからの現在の質問
    - **history**: 過去の会話履歴 (ChatMessageオブジェクトのリスト)
    - **conversation_id**: 会話の識別子 (新規会話の場合はNone)

    AIからの応答として、答えそのものではなく、考え方や調べ方の手順を返します。
    """
    print(f"API: Received request for /chat/thinking - Conversation ID: {request.conversation_id}, Question: {request.question[:50]}...")
    try:
        # Service Layer の関数を呼び出し、実際のビジネスロジックを実行
        response = await thinking_chat_service.process_thinking_request(db,request)

        # Service Layer から返された結果をそのまま返す
        return response

    except Exception as e:
        # Service Layer などで発生した例外をキャッチし、HTTPエラーとして返す
        print(f"API Error in /chat/thinking: {e}")
        # 本番環境では詳細なエラーメッセージをそのまま返さない方が良い場合が多い
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error processing thinking mode request"
        )

@router.post("/answer",
             response_model=ChatResponse,
             status_code=status.HTTP_200_OK,
             summary="答えを返した上で考え方を問うチャット機能"
            )
async def chat_answer_and_why_endpoint(request: ChatRequest, db: Session = Depends(get_db)):
    """
    **答え+なぜ？モード**のチャットリクエストを受け付けます。

    - **question**: ユーザーからの現在の質問
    - **history**: 過去の会話履歴 (ChatMessageオブジェクトのリスト)
    - **conversation_id**: 会話の識別子 (新規会話の場合はNone)

    AIからの応答として、まず質問への答えを返し、その後に答えの根拠や理由をユーザーに尋ねる質問を続けます。
    """
    print(f"API: Received request for /chat/answer - Question: {request.question[:50]}...")
    try:
        # Service Layer の関数を呼び出し、実際のビジネスロジックを実行
        response = await answer_chat_service.process_answer_and_why_request(db, request)

        # Service Layer から返された結果をそのまま返す
        return response

    except Exception as e:
        # Service Layer などで発生した例外をキャッチし、HTTPエラーとして返す
        print(f"API Error in /chat/answer: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error processing answer and why mode request"
        )

@router.post("/understanding_evaluation",
             response_model=ChatResponse, # 返すレスポンスの形式を指定 (自動で検証・整形)
             status_code=status.HTTP_200_OK, # 成功時のステータスコード
             summary="理解度を回答するチャット機能" # 自動生成ドキュメント用
            )
async def chat_understanding_evaluation_endpoint(request: ChatRequest, db: Session = Depends(get_db)):
    """
    **理解度評価モード**のチャットリクエストを受け付けます。

    - **question**: ユーザーからの現在の質問
    - **history**: 過去の会話履歴 (ChatMessageオブジェクトのリスト)
    - **conversation_id**: 会話の識別子 (新規会話の場合はNone)

    AIからの応答として、学習内容の理解度を返します。
    """
    print(f"API: Received request for /chat/understanding_evaluation - Conversation ID: {request.conversation_id}, Question: {request.question[:50]}...")
    try:
        # Service Layer の関数を呼び出し、実際のビジネスロジックを実行
        response = await understanding_evaluation_chat_service.process_understanding_evaluation_request(db,request)

        # Service Layer から返された結果をそのまま返す
        return response

    except Exception as e:
        # Service Layer などで発生した例外をキャッチし、HTTPエラーとして返す
        print(f"API Error in /chat/understanding_evaluation: {e}")
        # 本番環境では詳細なエラーメッセージをそのまま返さない方が良い場合が多い
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error processing understanding evaluation mode request"
        )
    

@router.post("/question",
            response_model=ChatResponse, # 返すレスポンスの形式を指定 (自動で検証・整形)
            status_code=status.HTTP_200_OK, # 成功時のステータスコード
            summary="理解度チェックの出題" # 自動生成ドキュメント用
            )
async def chat_question_endpoint(request: ChatRequest, db: Session = Depends(get_db)):
    """
    **理解度確認出題**のリクエストを受け付けます。

    - **question**: 対象の問題（学習した内容）
    - **history**: 過去の会話履歴 (ChatMessageオブジェクトのリスト)
    - **conversation_id**: 会話の識別子 (新規会話の場合はNone)

    AIからの応答として、学習内容の理解度を返します。
    """
    print(f"API: Received request for /chat/question - Conversation ID: {request.conversation_id}, Question: {request.question[:50]}...")
    try:
        # Service Layer の関数を呼び出し、実際のビジネスロジックを実行
        response = await question_chat_service.process_question_request(db, request)

    # Service Layer から返された結果をそのまま返す
        return response

    except Exception as e:
    # Service Layer などで発生した例外をキャッチし、HTTPエラーとして返す
        print(f"API Error in /chat/question: {e}")
        # 本番環境では詳細なエラーメッセージをそのまま返さない方が良い場合が多い
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error processing question request"
        )

# --- 必要に応じて他のチャット関連APIエンドポイントを追加 ---
# 例: /chat/history (履歴取得), /chat/new (新しい会話開始) など