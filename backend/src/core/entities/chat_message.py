"""
Chat Message Entity - Domain Model
"""

from dataclasses import dataclass, field
from typing import Optional, Dict, Any, List
from datetime import datetime


@dataclass
class ChatMessage:
    id: str
    user_id: str
    role: str  # "user" or "assistant"
    content: str
    created_at: datetime = field(default_factory=datetime.utcnow)
    conversation_id: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "user_id": self.user_id,
            "role": self.role,
            "content": self.content,
            "created_at": self.created_at.isoformat(),
            "conversation_id": self.conversation_id,
            "metadata": self.metadata
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ChatMessage":
        created_at = data.get("created_at")
        if isinstance(created_at, str):
            created_at = datetime.fromisoformat(created_at)
        elif not isinstance(created_at, datetime):
            created_at = datetime.utcnow()
            
        return cls(
            id=data.get("id", ""),
            user_id=data.get("user_id", ""),
            role=data.get("role", "user"),
            content=data.get("content", ""),
            created_at=created_at,
            conversation_id=data.get("conversation_id"),
            metadata=data.get("metadata", {})
        )


@dataclass
class ChatConversation:
    id: str
    user_id: str
    title: str = "New Conversation"
    messages: List[ChatMessage] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "user_id": self.user_id,
            "title": self.title,
            "messages": [m.to_dict() for m in self.messages],
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ChatConversation":
        created_at = data.get("created_at")
        if isinstance(created_at, str):
            created_at = datetime.fromisoformat(created_at)
        elif not isinstance(created_at, datetime):
            created_at = datetime.utcnow()
            
        updated_at = data.get("updated_at")
        if isinstance(updated_at, str):
            updated_at = datetime.fromisoformat(updated_at)
        elif not isinstance(updated_at, datetime):
            updated_at = datetime.utcnow()
            
        return cls(
            id=data.get("id", ""),
            user_id=data.get("user_id", ""),
            title=data.get("title", "New Conversation"),
            messages=[ChatMessage.from_dict(m) for m in data.get("messages", [])],
            created_at=created_at,
            updated_at=updated_at
        )
    
    def add_message(self, message: ChatMessage):
        self.messages.append(message)
        self.updated_at = datetime.utcnow()
