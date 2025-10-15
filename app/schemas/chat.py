from pydantic import BaseModel
from datetime import datetime
from typing import List


class ChatMessage(BaseModel):
    message: str


class ChatResponse(BaseModel):
    response: str


class MessageHistory(BaseModel):
    role: str
    content: str
    timestamp: datetime


class ConversationHistory(BaseModel):
    conversation_id: int
    messages: List[MessageHistory]


class AllConversationsHistory(BaseModel):
    conversations: List[ConversationHistory]
