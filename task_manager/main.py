"""Interactive CLI for Task Manager."""

from __future__ import annotations

import sys
from pathlib import Path

from models import (
    InvalidTransitionError,
    Priority,
    Status,
    Task,
    TaskError,
    TaskNotFoundError,
    ValidationError,
)
from repository import FileTaskRepository, InMemoryTaskRepository
from services import TaskService


# ── Display helpers ───────────────────────────────────────────────────────────

def clear_line() -> None:
    print()


def header(text: str) -> None:
    print(f"\n{'─' * 55}")
    print(f"  {text}")
    print(f"{'─' * 55}")


def show_menu() -> None:
    print("\n╔══════════════════════════════════════════╗")
    print("║       TASK MANAGER — Type-Safe CLI       ║")
    print("╠══════════════════════════════════════════╣")
    print("║  1. Create task          6. Cancel task  ║")
    print("║  2. List all tasks       7. Search       ║")
    print("║  3. Filter by status     8. Add tags     ║")
    print("║  4. Start task           9. Statistics   ║")
    print("║  5. Complete task       10. Delete task  ║")
    print("║                          0. Exit         ║")
    print("╚══════════════════════════════════════════╝")


def show_tasks(tasks: list[Task]) -> None:
    """Print a numbered list of tasks."""
    if not tasks:
        print("  (no tasks found)")
        return
    for i, task in enumerate(tasks, 1):
        print(f"  {i:>2}. {task}")
        print(f"       ID: {task.task_id}")
        if task.description:
            desc = task.description[:70] + ("…" if len(task.description) > 70 else "")
            print(f"       {desc}")


# ── Input helpers ─────────────────────────────────────────────────────────────

def ask(prompt: str, default: str = "") -> str:
    """Prompt user and return stripped input (or default)."""
    suffix = f" [{default}]" if default else ""
    result = input(f"  {prompt}{suffix}: ").strip()
    return result if result else default


def pick_task(service: TaskService) -> str:
    """Show task list and return full task_id chosen by user."""
    tasks = service.list_tasks()
    if not tasks:
        raise TaskNotFoundError("No tasks exist yet.")

    show_tasks(tasks)
    partial = ask("Enter task number OR first chars of ID").upper()

    # Try by list number first
    if partial.isdigit():
        idx = int(partial) - 1
        if 0 <= idx < len(tasks):
            return tasks[idx].task_id
        raise TaskNotFoundError(f"No task at position {partial}.")

    # Try by ID prefix
    matches = [t for t in tasks if t.task_id.upper().startswith(partial)]
    if len(matches) == 1:
        return matches[0].task_id
    if len(matches) > 1:
        print("  Multiple matches:")
        for m in matches:
            print(f"    {m.task_id[:12]}…  —  {m.title}")
        full_id = ask("Enter full ID")
        return full_id

    raise TaskNotFoundError(f"No task found starting with '{partial}'.")


# ── Handlers ──────────────────────────────────────────────────────────────────

def handle_create(service: TaskService) -> None:
    header("Create New Task")
    title       = ask("Title")
    description = ask("Description (optional)")
    priority    = ask("Priority (low/medium/high/critical)", "medium")
    tags_raw    = ask("Tags, comma-separated (optional)")
    tags        = [t.strip() for t in tags_raw.split(",") if t.strip()]

    task = service.create_task(title, description, priority, tags)
    print(f"\n  ✔ Created: {task}")
    print(f"    Full ID : {task.task_id}")


def handle_list_all(service: TaskService) -> None:
    tasks = service.list_tasks()
    header(f"All Tasks  ({len(tasks)} total)")
    show_tasks(tasks)


def handle_filter_by_status(service: TaskService) -> None:
    header("Filter by Status")
    values = [s.value for s in Status]
    print(f"  Statuses: {values}")
    status_str = ask("Status")
    try:
        status = Status(status_str.lower())
    except ValueError:
        print(f"  ✖ Invalid status '{status_str}'. Choose from {values}.")
        return
    tasks = service.list_tasks(status=status)
    header(f"Tasks with status '{status.value}'  ({len(tasks)} found)")
    show_tasks(tasks)


def handle_start(service: TaskService) -> None:
    header("Start Task")
    task_id = pick_task(service)
    task = service.start_task(task_id)
    print(f"\n  ✔ Started: {task}")


def handle_complete(service: TaskService) -> None:
    header("Complete Task")
    task_id = pick_task(service)
    task = service.complete_task(task_id)
    print(f"\n  ✔ Completed: {task}")


def handle_cancel(service: TaskService) -> None:
    header("Cancel Task")
    task_id = pick_task(service)
    task = service.cancel_task(task_id)
    print(f"\n  ✔ Cancelled: {task}")


def handle_search(service: TaskService) -> None:
    header("Search Tasks")
    query = ask("Search query")
    results = service.search_tasks(query)
    header(f"Results for '{query}'  ({len(results)} found)")
    show_tasks(results)


def handle_add_tags(service: TaskService) -> None:
    header("Add Tags")
    task_id  = pick_task(service)
    tags_raw = ask("New tags, comma-separated")
    tags     = [t.strip() for t in tags_raw.split(",") if t.strip()]
    task     = service.add_tags(task_id, tags)
    print(f"\n  ✔ Updated: {task}")


def handle_statistics(service: TaskService) -> None:
    header("Statistics")
    # Mypy knows this returns str because of @overload
    text: str = service.get_statistics("string")
    print(text)

    # Mypy knows this returns dict because of @overload
    stats: dict[str, int] = service.get_statistics("dict")
    total = stats["total"]
    done  = stats.get("done", 0)
    rate  = (done / total * 100) if total > 0 else 0.0
    print(f"\n  Completion rate : {rate:.1f}%  ({done}/{total} done)")


def handle_delete(service: TaskService) -> None:
    header("Delete Task")
    task_id = pick_task(service)
    confirm = ask("Are you sure? (yes/no)", "no")
    if confirm.lower() in ("yes", "y"):
        deleted = service.delete_task(task_id)
        if deleted:
            print("  ✔ Task deleted.")
        else:
            print("  ✖ Task not found.")
    else:
        print("  Cancelled — nothing deleted.")


# ── Demo data ─────────────────────────────────────────────────────────────────

def seed_demo_tasks(service: TaskService) -> None:
    """Populate with a few sample tasks."""
    demos: list[tuple[str, str, str, list[str]]] = [
        ("Set up CI/CD pipeline",
         "Configure GitHub Actions with Ruff + Mypy",
         "high", ["devops", "automation"]),
        ("Write unit tests",
         "Achieve 90% coverage using pytest",
         "critical", ["testing", "quality"]),
        ("Update README",
         "Add type annotation examples and setup instructions",
         "medium", ["docs"]),
        ("Fix login bug",
         "Users with special characters in password can't log in",
         "high", ["bug", "auth"]),
        ("Refactor database layer",
         "Move to repository pattern",
         "low", ["refactor", "db"]),
    ]
    for title, desc, prio, tags in demos:
        service.create_task(title, desc, prio, tags)
    print(f"  ✔ {len(demos)} demo tasks created.")


# ── Main loop ─────────────────────────────────────────────────────────────────

HANDLERS: dict[str, object] = {}   # filled after functions are defined


def run(use_file: bool = False) -> None:
    """Entry point."""
    if use_file:
        repo = FileTaskRepository(Path("tasks.json"))
        print("  Storage : tasks.json (persistent)")
    else:
        repo = InMemoryTaskRepository()
        print("  Storage : in-memory (resets on exit)")

    service = TaskService(repo)

    if repo.count() == 0:
        print("  Seeding demo tasks…")
        seed_demo_tasks(service)

    dispatch: dict[str, object] = {
        "1":  handle_create,
        "2":  handle_list_all,
        "3":  handle_filter_by_status,
        "4":  handle_start,
        "5":  handle_complete,
        "6":  handle_cancel,
        "7":  handle_search,
        "8":  handle_add_tags,
        "9":  handle_statistics,
        "10": handle_delete,
    }

    while True:
        show_menu()
        choice = input("  Choice: ").strip()

        if choice == "0":
            print("\n  Goodbye!\n")
            sys.exit(0)

        handler = dispatch.get(choice)
        if handler is None:
            print("  ✖ Invalid choice — try again.")
            continue

        try:
            # All handlers have the same signature: (TaskService) -> None
            if callable(handler):
                handler(service)  # type: ignore[call-arg]
        except ValidationError as exc:
            print(f"\n  ✖ Validation error : {exc}")
        except TaskNotFoundError as exc:
            print(f"\n  ✖ Not found        : {exc}")
        except InvalidTransitionError as exc:
            print(f"\n  ✖ Bad transition   : {exc}")
        except TaskError as exc:
            print(f"\n  ✖ Task error       : {exc}")
        except KeyboardInterrupt:
            print("\n\n  Interrupted. Goodbye!\n")
            sys.exit(0)


if __name__ == "__main__":
    use_file_storage = "--file" in sys.argv
    run(use_file=use_file_storage)