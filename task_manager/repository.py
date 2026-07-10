"""Repository layer — storage abstractions."""

from __future__ import annotations

import json
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Generic, TypeVar

from models import Task, TaskDict, TaskNotFoundError

T = TypeVar("T")


class Repository(ABC, Generic[T]):
    """Generic abstract repository."""

    @abstractmethod
    def add(self, item: T) -> None: ...

    @abstractmethod
    def get(self, item_id: str) -> T: ...

    @abstractmethod
    def get_all(self) -> list[T]: ...

    @abstractmethod
    def update(self, item: T) -> None: ...

    @abstractmethod
    def delete(self, item_id: str) -> bool: ...

    @abstractmethod
    def count(self) -> int: ...


class InMemoryTaskRepository(Repository[Task]):
    """Stores tasks in a Python dict (lost on exit)."""

    def __init__(self) -> None:
        self._tasks: dict[str, Task] = {}

    def add(self, item: Task) -> None:
        if item.task_id in self._tasks:
            raise ValueError(f"Task '{item.task_id}' already exists.")
        self._tasks[item.task_id] = item

    def get(self, item_id: str) -> Task:
        task = self._tasks.get(item_id)
        if task is None:
            raise TaskNotFoundError(f"No task with ID '{item_id}'.")
        return task

    def get_all(self) -> list[Task]:
        return list(self._tasks.values())

    def update(self, item: Task) -> None:
        if item.task_id not in self._tasks:
            raise TaskNotFoundError(f"No task with ID '{item.task_id}'.")
        self._tasks[item.task_id] = item

    def delete(self, item_id: str) -> bool:
        if item_id in self._tasks:
            del self._tasks[item_id]
            return True
        return False

    def count(self) -> int:
        return len(self._tasks)


class FileTaskRepository(Repository[Task]):
    """Persists tasks to a JSON file."""

    def __init__(self, file_path: Path) -> None:
        self._path = file_path
        self._tasks: dict[str, Task] = {}
        self._load()

    def _load(self) -> None:
        if self._path.exists():
            raw = self._path.read_text(encoding="utf-8").strip()
            if raw:
                data: list[TaskDict] = json.loads(raw)
                self._tasks = {
                    t["task_id"]: Task.from_dict(t) for t in data
                }

    def _save(self) -> None:
        data: list[TaskDict] = [t.to_dict() for t in self._tasks.values()]
        self._path.write_text(
            json.dumps(data, indent=2, ensure_ascii=False),
            encoding="utf-8",
        )

    def add(self, item: Task) -> None:
        if item.task_id in self._tasks:
            raise ValueError(f"Task '{item.task_id}' already exists.")
        self._tasks[item.task_id] = item
        self._save()

    def get(self, item_id: str) -> Task:
        task = self._tasks.get(item_id)
        if task is None:
            raise TaskNotFoundError(f"No task with ID '{item_id}'.")
        return task

    def get_all(self) -> list[Task]:
        return list(self._tasks.values())

    def update(self, item: Task) -> None:
        if item.task_id not in self._tasks:
            raise TaskNotFoundError(f"No task with ID '{item.task_id}'.")
        self._tasks[item.task_id] = item
        self._save()

    def delete(self, item_id: str) -> bool:
        if item_id in self._tasks:
            del self._tasks[item_id]
            self._save()
            return True
        return False

    def count(self) -> int:
        return len(self._tasks)