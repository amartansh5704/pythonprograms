"""Tests for the task manager — also fully typed."""

from __future__ import annotations

import pytest

from task_manager.models import (
    InvalidTransitionError,
    Priority,
    Status,
    Task,
    ValidationError,
)
from task_manager.repository import InMemoryTaskRepository
from task_manager.services import TaskService
from task_manager.validators import validate_tags, validate_title


# -- Fixtures --

@pytest.fixture
def service() -> TaskService:
    """Create a fresh TaskService with in-memory repo."""
    repo = InMemoryTaskRepository()
    return TaskService(repo)


@pytest.fixture
def sample_task(service: TaskService) -> Task:
    """Create a sample task."""
    return service.create_task(
        title="Test Task",
        description="A test task",
        priority="high",
        tags=["test", "sample"],
    )


# -- Model Tests --

class TestTask:
    """Tests for the Task model."""

    def test_create_task(self) -> None:
        task = Task(title="My Task", priority=Priority.HIGH)
        assert task.title == "My Task"
        assert task.priority == Priority.HIGH
        assert task.status == Status.TODO

    def test_valid_transition(self) -> None:
        task = Task(title="My Task")
        task.transition_to(Status.IN_PROGRESS)
        assert task.status == Status.IN_PROGRESS

    def test_invalid_transition(self) -> None:
        task = Task(title="My Task", status=Status.DONE)
        with pytest.raises(InvalidTransitionError):
            task.transition_to(Status.IN_PROGRESS)

    def test_serialization_roundtrip(self) -> None:
        original = Task(
            title="Roundtrip Test",
            description="Testing serialization",
            priority=Priority.CRITICAL,
            tags=["test"],
        )
        data = original.to_dict()
        restored = Task.from_dict(data)

        assert restored.title == original.title
        assert restored.priority == original.priority
        assert restored.tags == original.tags

    def test_str_representation(self) -> None:
        task = Task(title="Display Test", priority=Priority.HIGH, tags=["ui"])
        result = str(task)
        assert "Display Test" in result
        assert "high" in result
        assert "ui" in result


# -- Validator Tests --

class TestValidators:
    """Tests for validation functions."""

    def test_valid_title(self) -> None:
        assert validate_title("  Hello World  ") == "Hello World"

    def test_empty_title(self) -> None:
        with pytest.raises(ValidationError, match="cannot be empty"):
            validate_title("   ")

    def test_long_title(self) -> None:
        with pytest.raises(ValidationError, match="at most"):
            validate_title("x" * 201)

    def test_valid_tags(self) -> None:
        result = validate_tags(["Python", "  TYPE-CHECK  ", "python", ""])
        assert result == ["python", "type-check"]  # deduped, cleaned

    def test_invalid_tag_characters(self) -> None:
        with pytest.raises(ValidationError, match="invalid characters"):
            validate_tags(["valid", "inv@lid!"])


# -- Service Tests --

class TestTaskService:
    """Tests for the TaskService."""

    def test_create_task(self, service: TaskService) -> None:
        task = service.create_task("New Task", priority="high")
        assert task.title == "New Task"
        assert task.priority == Priority.HIGH

    def test_create_task_invalid_priority(self, service: TaskService) -> None:
        with pytest.raises(ValidationError, match="Invalid priority"):
            service.create_task("Task", priority="super_high")

    def test_list_by_status(self, service: TaskService, sample_task: Task) -> None:
        todos = service.list_tasks(status=Status.TODO)
        assert len(todos) == 1
        assert todos[0].task_id == sample_task.task_id

    def test_list_by_priority(self, service: TaskService, sample_task: Task) -> None:
        high_priority = service.list_tasks(priority=Priority.HIGH)
        assert len(high_priority) == 1

    def test_list_by_tag(self, service: TaskService, sample_task: Task) -> None:
        tagged = service.list_tasks(tag="test")
        assert len(tagged) == 1

    def test_start_task(self, service: TaskService, sample_task: Task) -> None:
        task = service.start_task(sample_task.task_id)
        assert task.status == Status.IN_PROGRESS

    def test_complete_task(self, service: TaskService, sample_task: Task) -> None:
        service.start_task(sample_task.task_id)
        task = service.complete_task(sample_task.task_id)
        assert task.status == Status.DONE

    def test_invalid_completion(self, service: TaskService, sample_task: Task) -> None:
        with pytest.raises(InvalidTransitionError):
            service.complete_task(sample_task.task_id)  # can't go TODO -> DONE

    def test_search(self, service: TaskService, sample_task: Task) -> None:
        results = service.search_tasks("test")
        assert len(results) == 1

    def test_search_no_results(self, service: TaskService, sample_task: Task) -> None:
        results = service.search_tasks("nonexistent_xyz")
        assert len(results) == 0

    def test_statistics_dict(self, service: TaskService, sample_task: Task) -> None:
        stats = service.get_statistics("dict")
        assert stats["total"] == 1
        assert stats["todo"] == 1

    def test_statistics_string(self, service: TaskService, sample_task: Task) -> None:
        stats = service.get_statistics("string")
        assert "total: 1" in stats
        assert isinstance(stats, str)

    def test_delete_task(self, service: TaskService, sample_task: Task) -> None:
        assert service.delete_task(sample_task.task_id) is True
        assert len(service.list_tasks()) == 0

    def test_add_tags(self, service: TaskService, sample_task: Task) -> None:
        task = service.add_tags(sample_task.task_id, ["new-tag", "another"])
        assert "new-tag" in task.tags
        assert "another" in task.tags


# -- Repository Tests --

class TestInMemoryRepository:
    """Tests for the InMemoryTaskRepository."""

    def test_add_duplicate_raises(self) -> None:
        repo = InMemoryTaskRepository()
        task = Task(title="Dup Test")
        repo.add(task)
        with pytest.raises(ValueError, match="already exists"):
            repo.add(task)

    def test_count(self) -> None:
        repo = InMemoryTaskRepository()
        assert repo.count() == 0
        repo.add(Task(title="Task 1"))
        repo.add(Task(title="Task 2"))
        assert repo.count() == 2