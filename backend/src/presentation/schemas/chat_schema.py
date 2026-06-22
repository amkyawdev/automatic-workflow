"""
Chat Schemas - Pydantic Models for Chat
"""

from pydantic import BaseModel, Field
from typing import Optional, List


class ChatMessageRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=5000)
    conversation_id: Optional[str] = None


class ChatMessageResponse(BaseModel):
    message: str
    suggestions: List[str] = []
    conversation_id: Optional[str] = None


class ChatHistoryResponse(BaseModel):
    id: str
    role: str
    content: str
    created_at: str
    conversation_id: Optional[str] = None


class ChatSuggestion(BaseModel):
    id: str
    text: str
