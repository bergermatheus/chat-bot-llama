from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.core.dependencies import get_current_user
from app.schemas.chat import (
    ChatMessage,
    ChatResponse,
    ConversationHistory,
    AllConversationsHistory,
)
from app.services.chat_service import chat_service
from app.models.conversation import Conversation
from app.models.message import Message
from typing import Optional

router = APIRouter()


@router.post("/chat", response_model=ChatResponse)
async def chat(
    chat_msg: ChatMessage,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    try:
        response = chat_service.process_chat(
            current_user.id, chat_msg.message, db
        )
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/conversation/history")
async def get_conversation_history(
    conversation_id: Optional[int] = Query(
        None,
        description="Conversation ID to retrieve. If not provided, returns all conversations.",
    ),
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    result = chat_service.get_conversation_history_for_api(
        current_user.id, conversation_id, db
    )

    if conversation_id:
        return ConversationHistory(**result)
    else:
        return AllConversationsHistory(**result)


@router.delete("/conversation/clear")
async def clear_conversation(
    current_user=Depends(get_current_user), db: Session = Depends(get_db)
):
    return chat_service.clear_conversation(current_user.id, db)
