from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Optional
from .workflow_state import WorkflowStatus, TaskPriority

@dataclass
class Task:
    id: str
    agent_id: str
    action: str
    data: Dict[str, Any]
    priority: TaskPriority = TaskPriority.NORMAL
    dependencies: List[str] = field(default_factory=list)
    timeout: int = 60
    retry_attempts: int = 3

    # Runtime
    status: WorkflowStatus = WorkflowStatus.PENDING
    result: Any = None
    error: Optional[str] = None
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    attempts: int = 0
