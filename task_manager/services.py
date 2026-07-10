"""Service layer — business logic."""

from __future__ import annotations

from typing import Callable, Literal, overload

from models import Priority, Status, Task
from repository import Repository
from validators import (
    validate_description,
    validate_priority_string,
    validate_tags,
    validate_title,
)

# Type alias
TaskFilter = Callable[[Task], bool]


class TaskService:
    """All business logic for the task manager."""

    def __init__(self, repository: Repository[Task]) -> None:
        self._repo = repository

    # ── CRUD ──────────────────────────────────────────────────────────────────

    def create_task(
        self,
        title: str,
        description: str = "",
        priority: str = "medium",
        tags: list[str] | None = None,
    ) -> Task:
        """Create and persist a new task."""
        task = Task(
            title=validate_title(title),
            description=validate_description(description),
            priority=validate_priority_string(priority),
            tags=validate_tags(tags or []),
        )
        self._repo.add(task)
        return task

    def get_task(self, task_id: str) -> Task:
        return self._repo.get(task_id)

    def delete_task(self, task_id: str) -> bool:
        return self._repo.delete(task_id)

    # ── Listing / Searching ───────────────────────────────────────────────────

    def list_tasks(
        self,
        *,
        status: Status | None = None,
        priority: Priority | None = None,
        tag: str | None = None,
    ) -> list[Task]:
        """Return tasks, optionally filtered."""
        tasks = self._repo.get_all()
        filters: list[TaskFilter] = []

        if status is not None:
            s = status
            filters.append(lambda t, _s=s: t.status == _s)  # type: ignore[misc]
        if priority is not None:
            p = priority
            filters.append(lambda t, _p=p: t.priority == _p)  # type: ignore[misc]
        if tag is not None:
            tg = tag.lower()
            filters.append(lambda t, _tg=tg: _tg in t.tags)  # type: ignore[misc]

        for f in filters:
            tasks = [t for t in tasks if f(t)]
        return tasks

    def search_tasks(self, query: str) -> list[Task]:
        """Full-text search on title and description."""
        q = query.lower()
        return [
            t for t in self._repo.get_all()
            if q in t.title.lower() or q in t.description.lower()
        ]

    # ── Status transitions ────────────────────────────────────────────────────

    def update_status(self, task_id: str, new_status: Status) -> Task:
        task = self._repo.get(task_id)
        task.transition_to(new_status)
        self._repo.update(task)
        return task

    def start_task(self, task_id: str) -> Task:
        return self.update_status(task_id, Status.IN_PROGRESS)

    def complete_task(self, task_id: str) -> Task:
        return self.update_status(task_id, Status.DONE)

    def cancel_task(self, task_id: str) -> Task:
        return self.update_status(task_id, Status.CANCELLED)

    # ── Tags ──────────────────────────────────────────────────────────────────

    def add_tags(self, task_id: str, new_tags: list[str]) -> Task:
        task = self._repo.get(task_id)
        task.tags = validate_tags([*task.tags, *new_tags])
        self._repo.update(task)
        return task

    # ── Statistics (with @overload) ───────────────────────────────────────────

    @overload
    def get_statistics(self, format_as: Literal["dict"]) -> dict[str, int]: ...

    @overload
    def get_statistics(self, format_as: Literal["string"]) -> str: ...

    def get_statistics(
        self,
        format_as: Literal["dict", "string"] = "dict",
    ) -> dict[str, int] | str:
        """Task statistics in dict or string form."""
        tasks = self._repo.get_all()
        stats: dict[str, int] = {
            "total": len(tasks),
            **{s.value: sum(1 for t in tasks if t.status == s) for s in Status},
            **{
                f"priority_{p.value}": sum(1 for t in tasks if t.priority == p)
                for p in Priority
            },
        }
        if format_as == "string":
            lines = [f"  {k:<25} : {v}" for k, v in stats.items()]
            return "Task Statistics\n" + "-" * 35 + "\n" + "\n".join(lines)
        return stats