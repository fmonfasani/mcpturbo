from enum import Enum

class WorkflowStatus(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"

class TaskPriority(int, Enum):
    LOW = 1
    NORMAL = 2
    HIGH = 3
    CRITICAL = 4
