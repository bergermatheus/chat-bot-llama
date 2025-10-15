from typing import List, Dict, Tuple, Optional
from sqlalchemy.orm import Session
from app.models.conversation import Conversation
from app.models.message import Message
from app.services.ollama_service import OllamaService
from datetime import datetime


class ChatService:
    def __init__(self):
        self.ollama = OllamaService()

    def get_conversation_history(
        self, user_id: int, db: Session
    ) -> Tuple[List[Dict[str, str]], Conversation]:
        conversation = (
            db.query(Conversation)
            .filter(Conversation.user_id == user_id)
            .order_by(Conversation.updated_at.desc())
            .first()
        )

        if not conversation:
            return []

        messages = (
            db.query(Message)
            .filter(Message.conversation_id == conversation.id)
            .order_by(Message.timestamp)
            .all()
        )

        history = []
        if not messages:
            history.append(
                {
                    "role": "system",
                    "content": "You are a helpful AI assistant. Keep your responses concise and relevant to the user's questions.",
                }
            )
        else:
            for msg in messages:
                history.append({"role": msg.role, "content": msg.content})

        return history, conversation

    def get_conversation_by_id(
        self, user_id: int, conversation_id: int, db: Session
    ) -> Optional[Conversation]:
        return (
            db.query(Conversation)
            .filter(
                Conversation.user_id == user_id,
                Conversation.id == conversation_id,
            )
            .first()
        )

    def get_all_conversations(
        self, user_id: int, db: Session
    ) -> List[Conversation]:
        return (
            db.query(Conversation)
            .filter(Conversation.user_id == user_id)
            .order_by(Conversation.updated_at.desc())
            .all()
        )

    def get_messages_by_conversation_id(
        self, conversation_id: int, db: Session
    ) -> List[Message]:
        return (
            db.query(Message)
            .filter(Message.conversation_id == conversation_id)
            .order_by(Message.timestamp)
            .all()
        )

    def get_conversation_history_for_api(
        self, user_id: int, conversation_id: Optional[int], db: Session
    ) -> Dict:
        if conversation_id:
            conversation = self.get_conversation_by_id(
                user_id, conversation_id, db
            )
            if not conversation:
                return {"conversation_id": 0, "messages": []}

            messages = self.get_messages_by_conversation_id(
                conversation_id, db
            )
            return {
                "conversation_id": conversation.id,
                "messages": [
                    {
                        "role": msg.role,
                        "content": msg.content,
                        "timestamp": msg.timestamp,
                    }
                    for msg in messages
                ],
            }

        conversations = self.get_all_conversations(user_id, db)
        result = []

        for conv in conversations:
            messages = self.get_messages_by_conversation_id(conv.id, db)
            result.append(
                {
                    "conversation_id": conv.id,
                    "messages": [
                        {
                            "role": msg.role,
                            "content": msg.content,
                            "timestamp": msg.timestamp,
                        }
                        for msg in messages
                    ],
                }
            )

        return {"conversations": result}

    def save_message(
        self, conversation_id: int, role: str, content: str, db: Session
    ):
        message = Message(
            conversation_id=conversation_id, role=role, content=content
        )
        db.add(message)
        return message

    def process_chat(
        self, user_id: int, user_message: str, db: Session
    ) -> str:
        history, conversation = self.get_conversation_history(user_id, db)
        history.append({"role": "user", "content": user_message})

        self.save_message(conversation.id, "user", user_message, db)

        ai_response = self.ollama.chat(history)

        self.save_message(conversation.id, "assistant", ai_response, db)

        conversation.updated_at = datetime.utcnow()
        db.commit()

        return ai_response

    def clear_conversation(self, user_id: int, db: Session) -> Dict[str, str]:
        conversation = (
            db.query(Conversation)
            .filter(Conversation.user_id == user_id)
            .order_by(Conversation.updated_at.desc())
            .first()
        )

        if conversation:
            db.query(Message).filter(
                Message.conversation_id == conversation.id
            ).delete()
            db.commit()
            return {"message": "Conversation cleared"}

        return {"message": "No conversation to clear"}


chat_service = ChatService()
