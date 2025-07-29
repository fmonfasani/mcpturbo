from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Optional
from .workflow_state import WorkflowStatus
from .task_model import Task

@dataclass
class Workflow:
    id: str
    name: str
    tasks: List[Task]
    status: WorkflowStatus = WorkflowStatus.PENDING
    created_at: datetime = field(default_factory=datetime.utcnow)
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    context: Dict[str, Any] = field(default_factory=dict)

    def get_ready_tasks(self) -> List[Task]:
        ready_tasks = []
        for task in self.tasks:
            if task.status != WorkflowStatus.PENDING:
                continue

            deps_completed = all(
                any(t.id == dep_id and t.status == WorkflowStatus.COMPLETED for t in self.tasks)
                for dep_id in task.dependencies
            )

            if not task.dependencies or deps_completed:
                ready_tasks.append(task)

        ready_tasks.sort(key=lambda t: t.priority.value, reverse=True)
        return ready_tasks

    def is_completed(self) -> bool:
        return all(task.status in [WorkflowStatus.COMPLETED, WorkflowStatus.FAILED] for task in self.tasks)

    def has_failed(self) -> bool:
        return any(task.status == WorkflowStatus.FAILED for task in self.tasks)
