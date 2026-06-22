"""
PostgreSQL Repository - Database Operations
"""

from typing import List, Optional, Dict, Any
from src.core.entities.workflow import Workflow
from src.core.entities.user import User
from src.core.entities.integration import Integration
from src.core.entities.chat_message import ChatMessage, ChatConversation
from src.utils.logger import logger


class DatabaseConnection:
    """Mock database connection - Replace with real SQLAlchemy"""
    def __init__(self):
        self._storage: Dict[str, Dict[str, Any]] = {
            "workflows": {},
            "users": {},
            "integrations": {},
            "chat_messages": {}
        }
    
    async def execute(self, query: str, params: tuple = None):
        """Execute a query (mock)"""
        pass


class WorkflowRepository:
    def __init__(self):
        self._workflows: Dict[str, Workflow] = {}
    
    async def create(self, workflow: Workflow) -> Workflow:
        self._workflows[workflow.id] = workflow
        logger.info(f"Created workflow: {workflow.id}")
        return workflow
    
    async def get_by_id(self, workflow_id: str) -> Optional[Workflow]:
        return self._workflows.get(workflow_id)
    
    async def get_by_user(self, user_id: str, skip: int = 0, limit: int = 100) -> List[Workflow]:
        workflows = [w for w in self._workflows.values() if w.user_id == user_id]
        return workflows[skip:skip + limit]
    
    async def update(self, workflow: Workflow) -> Workflow:
        self._workflows[workflow.id] = workflow
        return workflow
    
    async def delete(self, workflow_id: str) -> bool:
        if workflow_id in self._workflows:
            del self._workflows[workflow_id]
            return True
        return False


class UserRepository:
    def __init__(self):
        self._users: Dict[str, User] = {}
    
    async def create(self, user: User, password: str) -> User:
        from passlib.context import CryptContext
        pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        # bcrypt has a 72 bytes limit
        password_bytes = password.encode('utf-8')[:72].decode('utf-8', errors='ignore')
        user.hashed_password = pwd_context.hash(password_bytes)
        self._users[user.id] = user
        logger.info(f"Created user: {user.id}")
        return user
    
    async def get_by_id(self, user_id: str) -> Optional[User]:
        return self._users.get(user_id)
    
    async def get_by_email(self, email: str) -> Optional[User]:
        for user in self._users.values():
            if user.email == email:
                return user
        return None
    
    async def update(self, user: User) -> User:
        self._users[user.id] = user
        return user


class IntegrationRepository:
    def __init__(self):
        self._integrations: Dict[str, Integration] = {}
    
    async def create(self, integration: Integration) -> Integration:
        self._integrations[integration.id] = integration
        logger.info(f"Created integration: {integration.id}")
        return integration
    
    async def get_by_id(self, integration_id: str) -> Optional[Integration]:
        return self._integrations.get(integration_id)
    
    async def get_by_user(self, user_id: str) -> List[Integration]:
        return [i for i in self._integrations.values() if i.user_id == user_id]
    
    async def delete(self, integration_id: str) -> bool:
        if integration_id in self._integrations:
            del self._integrations[integration_id]
            return True
        return False


class ChatRepository:
    def __init__(self):
        self._messages: Dict[str, ChatMessage] = {}
    
    async def save_message(self, message: ChatMessage) -> ChatMessage:
        self._messages[message.id] = message
        return message
    
    async def get_history(self, user_id: str, limit: int = 50) -> List[ChatMessage]:
        messages = [m for m in self._messages.values() if m.user_id == user_id]
        messages.sort(key=lambda x: x.created_at)
        return messages[-limit:]


# Initialize database connection
db_connection = DatabaseConnection()


async def init_database():
    """Initialize database connection"""
    logger.info("Initializing database...")
    # In production, initialize SQLAlchemy engine here
    pass
