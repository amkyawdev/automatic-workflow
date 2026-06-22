"""
Workflow Schemas - Pydantic Models for Request/Response
"""

from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List


class TriggerSchema(BaseModel):
    type: str
    config: Dict[str, Any] = Field(default_factory=dict)


class ActionSchema(BaseModel):
    service: str
    action: str
    parameters: Dict[str, Any] = Field(default_factory=dict)
    order: int = 0


class WorkflowCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = Field(None, max_length=1000)
    trigger: Optional[Dict[str, Any]] = None
    actions: Optional[List[Dict[str, Any]]] = None


class WorkflowUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = Field(None, max_length=1000)
    status: Optional[str] = None
    trigger: Optional[Dict[str, Any]] = None
    actions: Optional[List[Dict[str, Any]]] = None


class WorkflowExecute(BaseModel):
    parameters: Optional[Dict[str, Any]] = None


class WorkflowResponse(BaseModel):
    id: str
    name: str
    description: str
    user_id: str
    status: str
    trigger: Optional[Dict[str, Any]] = None
    actions: List[Dict[str, Any]] = []
    created_at: str
    updated_at: str
    last_run: Optional[str] = None
    execution_count: int = 0
    success_count: int = 0
    failure_count: int = 0
    success_rate: float = 100.0

    class Config:
        from_attributes = True
