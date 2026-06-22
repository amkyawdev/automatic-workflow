"""
Integration Schemas - Pydantic Models
"""

from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from datetime import datetime


class IntegrationConnect(BaseModel):
    service: str = Field(..., description="Service name (openai, slack, discord, etc.)")
    api_key: str = Field(..., description="API key for the service")
    config: Optional[Dict[str, Any]] = Field(default_factory=dict)


class IntegrationResponse(BaseModel):
    id: str
    user_id: str
    service: str
    name: str
    is_connected: bool
    created_at: str
    updated_at: str

    class Config:
        from_attributes = True
