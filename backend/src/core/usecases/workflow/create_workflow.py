"""
Create Workflow Use Case
"""

from src.core.entities.workflow import Workflow
from src.infrastructure.database.postgres_repository import WorkflowRepository


class CreateWorkflowUseCase:
    def __init__(self, repository: WorkflowRepository):
        self.repository = repository
    
    async def execute(self, workflow: Workflow) -> Workflow:
        """Create a new workflow"""
        return await self.repository.create(workflow)
