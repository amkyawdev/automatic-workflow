"""
Integration Entity - Domain Model
"""

from dataclasses import dataclass, field
from typing import Dict, Any, Optional
from datetime import datetime


@dataclass
class Integration:
    id: str
    user_id: str
    service: str
    name: str
    encrypted_api_key: str = ""
    config: Dict[str, Any] = field(default_factory=dict)
    is_connected: bool = True
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "user_id": self.user_id,
            "service": self.service,
            "name": self.name,
            "is_connected": self.is_connected,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Integration":
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
            
        return cls(
            id=data.get("id", ""),
            user_id=data.get("user_id", ""),
            service=data.get("service", ""),
            name=data.get("name", ""),
            encrypted_api_key=data.get("encrypted_api_key", ""),
            config=data.get("config", {}),
            is_connected=data.get("is_connected", True),
            created_at=created_at,
            updated_at=updated_at
        )
