"""Domain models with full type annotations."""

from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Final, TypedDict


class Priority(Enum):
    """Task priority levels."""

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class Status(Enum):
    """Task status lifecycle."""

    TODO = "todo"
    IN_PROGRESS = "in_progress"
    DONE = "done"
    CANCELLED = "cancelled"


MAX_TITLE_LENGTH: Final[int] = 200
MAX_DESCRIPTION_LENGTH: Final[int] = 2000

VALID_TRANSITIONS: Final[dict[Status, list[Status]]] = {
    Status.TODO: [Status.IN_PROGRESS, Status.CANCELLED],
    Status.IN_PROGRESS: [Status.DONE, Status.TODO, Status.CANCELLED],
    Status.DONE: [],
    Status.CANCELLED: [Status.TODO],
}


class TaskDict(TypedDict):
    """Dictionary representation of a Task."""

    task_id: str
    title: str
    description: str
    priority: str
    status: str
    tags: list[str]
    created_at: str
    updated_at: str


@dataclass
class Task:
    """Represents a task in the system."""

    title: str
    description: str = ""
    priority: Priority = Priority.MEDIUM
    status: Status = Status.TODO
    tags: list[str] = field(default_factory=list)
    task_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)

    def transition_to(self, new_status: Status) -> None:
        """Transition task to a new status."""
        allowed = VALID_TRANSITIONS.get(self.status, [])
        if new_status not in allowed:
            allowed_names = [s.value for s in allowed]
            msg = (
                f"Cannot transition from '{self.status.value}' "
                f"to '{new_status.value}'. "
                f"Allowed transitions: {allowed_names}"
            )
            raise InvalidTransitionError(msg)
        self.status = new_status
        self.updated_at = datetime.now()

    def to_dict(self) -> TaskDict:
        """Serialize task to dictionary."""
        return TaskDict(
            task_id=self.task_id,
            title=self.title,
            description=self.description,
            priority=self.priority.value,
            status=self.status.value,
            tags=list(self.tags),
            created_at=self.created_at.isoformat(),
            updated_at=self.updated_at.isoformat(),
        )

    @classmethod
    def from_dict(cls, data: TaskDict) -> Task:
        """Deserialize task from dictionary."""
        return cls(
            task_id=data["task_id"],
            title=data["title"],
            description=data["description"],
            priority=Priority(data["priority"]),
            status=Status(data["status"]),
            tags=data["tags"],
            created_at=datetime.fromisoformat(data["created_at"]),
            updated_at=datetime.fromisoformat(data["updated_at"]),
        )

    def __str__(self) -> str:
        tags_str = ", ".join(self.tags) if self.tags else "none"
        return (
            f"[{self.status.value.upper():12}] {self.title:<40} "
            f"| Priority: {self.priority.value:<8} "
            f"| Tags: {tags_str}"
        )


# ── Custom Exceptions ─────────────────────────────────────────────────────────

class TaskError(Exception):
    """Base exception for task errors."""


class InvalidTransitionError(TaskError):
    """Raised on invalid status transition."""


class ValidationError(TaskError):
    """Raised when validation fails."""


class TaskNotFoundError(TaskError):
    """Raised when a task is not found."""