"""
Workflow Entity - Domain Model
"""

from dataclasses import dataclass, field
from typing import Optional, Dict, Any, List
from enum import Enum


class WorkflowStatus(str, Enum):
    DRAFT = "draft"
    ACTIVE = "active"
    INACTIVE = "inactive"
    ERROR = "error"


class TriggerType(str, Enum):
    SCHEDULE = "schedule"
    WEBHOOK = "webhook"
    EVENT = "event"


@dataclass
class Trigger:
    type: TriggerType
    config: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "type": self.type.value,
            "config": self.config
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Trigger":
        return cls(
            type=TriggerType(data.get("type", "schedule")),
            config=data.get("config", {})
        )


@dataclass
class Action:
    service: str
    action: str
    parameters: Dict[str, Any] = field(default_factory=dict)
    order: int = 0
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "service": self.service,
            "action": self.action,
            "parameters": self.parameters,
            "order": self.order
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Action":
        return cls(
            service=data.get("service", ""),
            action=data.get("action", ""),
            parameters=data.get("parameters", {}),
            order=data.get("order", 0)
        )


@dataclass
class Workflow:
    id: str
    name: str
    description: str = ""
    user_id: str = ""
    status: WorkflowStatus = WorkflowStatus.DRAFT
    trigger: Optional[Trigger] = None
    actions: List[Action] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
    last_run: Optional[datetime] = None
    execution_count: int = 0
    success_count: int = 0
    failure_count: int = 0
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "user_id": self.user_id,
            "status": self.status.value,
            "trigger": self.trigger.to_dict() if self.trigger else None,
            "actions": [a.to_dict() for a in self.actions],
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "last_run": self.last_run.isoformat() if self.last_run else None,
            "execution_count": self.execution_count,
            "success_count": self.success_count,
            "failure_count": self.failure_count,
            "success_rate": self.get_success_rate()
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Workflow":
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
            
        last_run = data.get("last_run")
        if isinstance(last_run, str):
            last_run = datetime.fromisoformat(last_run)
            
        return cls(
            id=data.get("id", ""),
            name=data.get("name", ""),
            description=data.get("description", ""),
            user_id=data.get("user_id", ""),
            status=WorkflowStatus(data.get("status", "draft")),
            trigger=Trigger.from_dict(data["trigger"]) if data.get("trigger") else None,
            actions=[Action.from_dict(a) for a in data.get("actions", [])],
            created_at=created_at,
            updated_at=updated_at,
            last_run=last_run,
            execution_count=data.get("execution_count", 0),
            success_count=data.get("success_count", 0),
            failure_count=data.get("failure_count", 0)
        )
    
    def get_success_rate(self) -> float:
        if self.execution_count == 0:
            return 100.0
        return round((self.success_count / self.execution_count) * 100, 2)
    
    def record_success(self):
        self.execution_count += 1
        self.success_count += 1
        self.last_run = datetime.utcnow()
        self.updated_at = datetime.utcnow()
    
    def record_failure(self):
        self.execution_count += 1
        self.failure_count += 1
        self.last_run = datetime.utcnow()
        self.updated_at = datetime.utcnow()
