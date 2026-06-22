"""
Connect Service Use Case
"""

import uuid
from src.core.entities.integration import Integration
from src.infrastructure.database.postgres_repository import IntegrationRepository
from src.infrastructure.security.encryption import EncryptionService


class ConnectServiceUseCase:
    def __init__(self, repository: IntegrationRepository):
        self.repository = repository
        self.encryption = EncryptionService()
    
    async def execute(
        self, 
        user_id: str, 
        service: str, 
        api_key: str,
        config: dict = None
    ) -> Integration:
        """Connect a new integration"""
        # Encrypt the API key
        encrypted_key = self.encryption.encrypt(api_key)
        
        # Create integration
        integration = Integration(
            id=str(uuid.uuid4()),
            user_id=user_id,
            service=service,
            name=f"{service.title()} Integration",
            encrypted_api_key=encrypted_key,
            config=config or {}
        )
        
        # Validate credentials
        if not await self._validate_credentials(service, api_key):
            raise ValueError(f"Invalid credentials for {service}")
        
        return await self.repository.create(integration)
    
    async def _validate_credentials(self, service: str, api_key: str) -> bool:
        """Validate service credentials"""
        # Service-specific validation
        validators = {
            "openai": self._validate_openai,
            "slack": self._validate_slack,
            "discord": self._validate_discord,
            "github": self._validate_github,
            "notion": self._validate_notion,
            "google": self._validate_google
        }
        
        validator = validators.get(service)
        if validator:
            return await validator(api_key)
        
        return True  # Default to valid for unknown services
    
    async def _validate_openai(self, api_key: str) -> bool:
        """Validate OpenAI API key"""
        return api_key.startswith("sk-")
    
    async def _validate_slack(self, api_key: str) -> bool:
        """Validate Slack API key"""
        return api_key.startswith("xoxb-")
    
    async def _validate_discord(self, api_key: str) -> bool:
        """Validate Discord API key"""
        return len(api_key) > 50
    
    async def _validate_github(self, api_key: str) -> bool:
        """Validate GitHub token"""
        return len(api_key) > 30
    
    async def _validate_notion(self, api_key: str) -> bool:
        """Validate Notion API key"""
        return api_key.startswith("secret_")
    
    async def _validate_google(self, api_key: str) -> bool:
        """Validate Google API key"""
        return len(api_key) > 30
