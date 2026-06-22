"""
Workflow Routes - API Endpoints for Workflows
"""

from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Optional
import uuid

from src.core.entities.workflow import Workflow, WorkflowStatus
from src.core.usecases.workflow.create_workflow import CreateWorkflowUseCase
from src.core.usecases.workflow.execute_workflow import ExecuteWorkflowUseCase
from src.presentation.schemas.workflow_schema import (
    WorkflowCreate,
    WorkflowUpdate,
    WorkflowResponse,
    WorkflowExecute
)
from src.presentation.middleware.authentication import get_current_user
from src.infrastructure.database.postgres_repository import WorkflowRepository


router = APIRouter()
workflow_repo = WorkflowRepository()


@router.get("/", response_model=List[WorkflowResponse])
async def list_workflows(
    skip: int = 0,
    limit: int = 100,
    user_id: str = Depends(get_current_user)
):
    """List all workflows for the current user"""
    workflows = await workflow_repo.get_by_user(user_id, skip=skip, limit=limit)
    return [WorkflowResponse(**w.to_dict()) for w in workflows]


@router.get("/{workflow_id}", response_model=WorkflowResponse)
async def get_workflow(
    workflow_id: str,
    user_id: str = Depends(get_current_user)
):
    """Get a specific workflow by ID"""
    workflow = await workflow_repo.get_by_id(workflow_id)
    
    if not workflow:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Workflow not found"
        )
    
    if workflow.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this workflow"
        )
    
    return WorkflowResponse(**workflow.to_dict())


@router.post("/", response_model=WorkflowResponse, status_code=status.HTTP_201_CREATED)
async def create_workflow(
    workflow_data: WorkflowCreate,
    user_id: str = Depends(get_current_user)
):
    """Create a new workflow"""
    use_case = CreateWorkflowUseCase(workflow_repo)
    
    workflow = Workflow(
        id=str(uuid.uuid4()),
        name=workflow_data.name,
        description=workflow_data.description or "",
        user_id=user_id,
        status=WorkflowStatus.DRAFT
    )
    
    if workflow_data.trigger:
        from src.core.entities.workflow import Trigger
        workflow.trigger = Trigger.from_dict(workflow_data.trigger)
    
    created_workflow = await use_case.execute(workflow)
    return WorkflowResponse(**created_workflow.to_dict())


@router.put("/{workflow_id}", response_model=WorkflowResponse)
async def update_workflow(
    workflow_id: str,
    workflow_data: WorkflowUpdate,
    user_id: str = Depends(get_current_user)
):
    """Update an existing workflow"""
    workflow = await workflow_repo.get_by_id(workflow_id)
    
    if not workflow:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Workflow not found"
        )
    
    if workflow.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this workflow"
        )
    
    # Update fields
    if workflow_data.name is not None:
        workflow.name = workflow_data.name
    if workflow_data.description is not None:
        workflow.description = workflow_data.description
    if workflow_data.status is not None:
        workflow.status = WorkflowStatus(workflow_data.status)
    if workflow_data.trigger is not None:
        from src.core.entities.workflow import Trigger
        workflow.trigger = Trigger.from_dict(workflow_data.trigger)
    if workflow_data.actions is not None:
        from src.core.entities.workflow import Action
        workflow.actions = [Action.from_dict(a) for a in workflow_data.actions]
    
    updated_workflow = await workflow_repo.update(workflow)
    return WorkflowResponse(**updated_workflow.to_dict())


@router.delete("/{workflow_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_workflow(
    workflow_id: str,
    user_id: str = Depends(get_current_user)
):
    """Delete a workflow"""
    workflow = await workflow_repo.get_by_id(workflow_id)
    
    if not workflow:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Workflow not found"
        )
    
    if workflow.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this workflow"
        )
    
    await workflow_repo.delete(workflow_id)
    return None


@router.post("/{workflow_id}/execute", response_model=dict)
async def execute_workflow(
    workflow_id: str,
    execute_data: Optional[WorkflowExecute] = None,
    user_id: str = Depends(get_current_user)
):
    """Execute a workflow"""
    workflow = await workflow_repo.get_by_id(workflow_id)
    
    if not workflow:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Workflow not found"
        )
    
    if workflow.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to execute this workflow"
        )
    
    if workflow.status != WorkflowStatus.ACTIVE:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Workflow must be active to execute"
        )
    
    use_case = ExecuteWorkflowUseCase()
    result = await use_case.execute(workflow, execute_data.parameters if execute_data else None)
    
    # Record execution
    if result.get("success"):
        workflow.record_success()
    else:
        workflow.record_failure()
    await workflow_repo.update(workflow)
    
    return result
