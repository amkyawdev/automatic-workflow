"""
Authenticate User Use Case
"""

from typing import Optional, Tuple
from src.core.entities.user import User
from src.infrastructure.security.jwt_handler import JWTHandler


class AuthenticateUserUseCase:
    def __init__(self, user_repository, jwt_handler: JWTHandler):
        self.user_repository = user_repository
        self.jwt_handler = jwt_handler
    
    async def execute(self, email: str, password: str) -> Optional[Tuple[str, dict]]:
        """Authenticate user and return access token"""
        # Get user by email
        user = await self.user_repository.get_by_email(email)
        
        if not user:
            return None
        
        # Verify password
        from passlib.context import CryptContext
        pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        
        if not pwd_context.verify(password, user.hashed_password):
            return None
        
        # Check if user is active
        if not user.is_active:
            return None
        
        # Update last login
        user.last_login = datetime.utcnow()
        await self.user_repository.update(user)
        
        # Create access token
        access_token = self.jwt_handler.create_access_token(
            data={"sub": user.id, "email": user.email}
        )
        
        return access_token, {"user_id": user.id, "email": user.email}
