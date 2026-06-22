"""
Integration Routes - API Endpoints for Integrations
"""

from fastapi import APIRouter, Depends, HTTPException, status
from typing import List

from src.core.entities.integration import Integration
from src.core.usecases.integration.connect_service import ConnectServiceUseCase
from src.presentation.schemas.integration_schema import (
    IntegrationResponse,
    IntegrationConnect
)
from src.presentation.middleware.authentication import get_current_user
from src.infrastructure.database.postgres_repository import IntegrationRepository


router = APIRouter()
integration_repo = IntegrationRepository()


@router.get("/", response_model=List[IntegrationResponse])
async def list_integrations(
    user_id: str = Depends(get_current_user)
):
    """List all connected integrations for the current user"""
    integrations = await integration_repo.get_by_user(user_id)
    return [IntegrationResponse(**i.to_dict()) for i in integrations]


@router.post("/connect", response_model=IntegrationResponse, status_code=status.HTTP_201_CREATED)
async def connect_integration(
    data: IntegrationConnect,
    user_id: str = Depends(get_current_user)
):
    """Connect a new integration"""
    use_case = ConnectServiceUseCase(integration_repo)
    integration = await use_case.execute(user_id, data.service, data.api_key, data.config)
    return IntegrationResponse(**integration.to_dict())


@router.delete("/{integration_id}", status_code=status.HTTP_204_NO_CONTENT)
async def disconnect_integration(
    integration_id: str,
    user_id: str = Depends(get_current_user)
):
    """Disconnect an integration"""
    integration = await integration_repo.get_by_id(integration_id)
    
    if not integration:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Integration not found"
        )
    
    if integration.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this integration"
        )
    
    await integration_repo.delete(integration_id)
    return None
