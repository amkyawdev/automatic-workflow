"""
Chat Routes - API Endpoints for AI Chat Assistant
"""

from fastapi import APIRouter, Depends, HTTPException, status
from typing import List

from src.core.usecases.chat.process_message import ProcessMessageUseCase
from src.presentation.schemas.chat_schema import (
    ChatMessageRequest,
    ChatMessageResponse,
    ChatHistoryResponse,
    ChatSuggestion
)
from src.presentation.middleware.authentication import get_current_user
from src.infrastructure.database.postgres_repository import ChatRepository
from src.utils.config import settings


router = APIRouter()
chat_repo = ChatRepository()


@router.post("/", response_model=ChatMessageResponse)
async def send_message(
    request: ChatMessageRequest,
    user_id: str = Depends(get_current_user)
):
    """Send a message to the AI assistant"""
    use_case = ProcessMessageUseCase(chat_repo)
    
    response = await use_case.execute(user_id, request.message)
    
    return ChatMessageResponse(
        message=response["message"],
        suggestions=response.get("suggestions", []),
        conversation_id=response.get("conversation_id")
    )


@router.get("/history", response_model=List[ChatHistoryResponse])
async def get_history(
    limit: int = 50,
    user_id: str = Depends(get_current_user)
):
    """Get chat history for the current user"""
    history = await chat_repo.get_history(user_id, limit=limit)
    return [ChatHistoryResponse(**h.to_dict()) for h in history]


@router.get("/suggestions", response_model=List[ChatSuggestion])
async def get_suggestions():
    """Get suggested questions for the chat"""
    suggestions = [
        ChatSuggestion(id="1", text="How do I create my first workflow?"),
        ChatSuggestion(id="2", text="How to get an OpenAI API key?"),
        ChatSuggestion(id="3", text="Connect Slack integration"),
        ChatSuggestion(id="4", text="What integrations are available?"),
        ChatSuggestion(id="5", text="How to set up a webhook trigger?"),
    ]
    return suggestions


@router.post("/feedback")
async def submit_feedback(
    message_id: str,
    helpful: bool,
    user_id: str = Depends(get_current_user)
):
    """Submit feedback for a chat message"""
    # Store feedback (implementation depends on your needs)
    return {"status": "success", "message": "Feedback submitted"}
