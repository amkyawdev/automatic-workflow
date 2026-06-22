"""
Generate Token Use Case
"""

from typing import Tuple
from src.core.entities.user import User
from src.infrastructure.security.jwt_handler import JWTHandler


class GenerateTokenUseCase:
    def __init__(self, jwt_handler: JWTHandler):
        self.jwt_handler = jwt_handler
    
    def execute(self, user: User) -> Tuple[str, dict]:
        """Generate access token for user"""
        access_token = self.jwt_handler.create_access_token(
            data={"sub": user.id, "email": user.email}
        )
        return access_token, {"user_id": user.id, "email": user.email}
