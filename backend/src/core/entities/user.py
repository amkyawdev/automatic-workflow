"""
User Entity - Domain Model
"""

from dataclasses import dataclass, field
from typing import Optional, Dict, Any
from enum import Enum
from datetime import datetime


class UserPlan(str, Enum):
    FREE = "free"
    PRO = "pro"
    ENTERPRISE = "enterprise"


@dataclass
class User:
    id: str
    email: str
    name: str = ""
    hashed_password: str = ""
    plan: UserPlan = UserPlan.FREE
    is_active: bool = True
    is_verified: bool = False
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
    last_login: Optional[datetime] = None
    executions_used: int = 0
    
    # Limits by plan
    EXECUTION_LIMITS = {
        UserPlan.FREE: 100,
        UserPlan.PRO: -1,  # Unlimited
        UserPlan.ENTERPRISE: -1  # Unlimited
    }
    
    def to_dict(self, include_sensitive: bool = False) -> Dict[str, Any]:
        data = {
            "id": self.id,
            "email": self.email,
            "name": self.name,
            "plan": self.plan.value,
            "is_active": self.is_active,
            "is_verified": self.is_verified,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "last_login": self.last_login.isoformat() if self.last_login else None,
            "executions_used": self.executions_used,
            "executions_limit": self.get_execution_limit()
        }
        if include_sensitive:
            data["hashed_password"] = self.hashed_password
        return data
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "User":
        created_at = data.get("created_at")
        if isinstance(created_at, str):
            created_at = datetime.fromisoformat(created_at)
        elif not isinstance(created_at, datetime):
            created_at = datetime.utcnow()
            
        updated_at = data.get("updated_at")
        if isinstance(updated_at, str):
            updated_at = datetime.fromisoformat(updated_at)
        elif not isinstance(updated_at, datetime):
            updated_at = datetime.utcnow()
            
        last_login = data.get("last_login")
        if isinstance(last_login, str):
            last_login = datetime.fromisoformat(last_login)
            
        return cls(
            id=data.get("id", ""),
            email=data.get("email", ""),
            name=data.get("name", ""),
            hashed_password=data.get("hashed_password", ""),
            plan=UserPlan(data.get("plan", "free")),
            is_active=data.get("is_active", True),
            is_verified=data.get("is_verified", False),
            created_at=created_at,
            updated_at=updated_at,
            last_login=last_login,
            executions_used=data.get("executions_used", 0)
        )
    
    def get_execution_limit(self) -> int:
        return self.EXECUTION_LIMITS.get(self.plan, 100)
    
    def can_execute(self) -> bool:
        limit = self.get_execution_limit()
        if limit == -1:  # Unlimited
            return True
        return self.executions_used < limit
    
    def increment_execution(self):
        self.executions_used += 1
        self.updated_at = datetime.utcnow()
    
    def verify(self):
        self.is_verified = True
        self.updated_at = datetime.utcnow()
