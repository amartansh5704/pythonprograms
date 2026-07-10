"""
Student Grade Manager
─────────────────────
Demonstrates:
  - Type annotations (basic, list, dict, Optional, Union)
  - Enums with type safety
  - Dataclasses with typed fields
  - TypedDict for structured dicts
  - @overload for multiple return types
  - Custom exceptions
  - Mypy strict mode compliance
  - Ruff linting compliance
"""

from __future__ import annotations

# ─────────────────────────────────────────────────────────────────────────────
# IMPORTS
# stdlib only — no third-party needed
# ─────────────────────────────────────────────────────────────────────────────
import sys
from dataclasses import dataclass, field
from enum import Enum
from typing import Final, Literal, TypedDict, overload

# ─────────────────────────────────────────────────────────────────────────────
# CONSTANTS  (Final → mypy will error if you try to reassign these)
# ─────────────────────────────────────────────────────────────────────────────

# Final[int] means PASSING_MARK is a constant integer — cannot be changed later
PASSING_MARK: Final[int] = 40

# Final[int] — maximum allowed marks for any subject
MAX_MARK: Final[int] = 100

# Final[str] — app title used in display
APP_TITLE: Final[str] = "Student Grade Manager"


# ─────────────────────────────────────────────────────────────────────────────
# ENUM  (type-safe alternative to plain strings like "A", "B", "C")
# Mypy will catch typos like Grade("AA") at check time
# ─────────────────────────────────────────────────────────────────────────────

class Grade(Enum):
    """Letter grades with their minimum percentage threshold."""

    A_PLUS  = "A+"   # 90–100
    A       = "A"    # 80–89
    B       = "B"    # 70–79
    C       = "C"    # 60–69
    D       = "D"    # 50–59
    E       = "E"    # 40–49
    F       = "F"    # 0–39  (fail)


# ─────────────────────────────────────────────────────────────────────────────
# CUSTOM EXCEPTIONS
# Specific exception types let callers handle errors precisely.
# All inherit from a base so you can also catch them all at once.
# ─────────────────────────────────────────────────────────────────────────────

class GradeError(Exception):
    """Base exception for all grade-related errors."""


class InvalidMarkError(GradeError):
    """Raised when a mark is outside the 0–MAX_MARK range."""


class StudentNotFoundError(GradeError):
    """Raised when a student ID does not exist in the registry."""


class DuplicateStudentError(GradeError):
    """Raised when adding a student whose ID already exists."""


# ─────────────────────────────────────────────────────────────────────────────
# TYPED DICT  — describes the exact shape of a plain dict
# Useful for JSON serialization / passing data between functions
# Mypy checks that every key exists and has the correct type
# ─────────────────────────────────────────────────────────────────────────────

class SubjectResult(TypedDict):
    """One subject's result as a plain dictionary."""

    subject: str    # e.g. "Math"
    mark: int       # 0–100
    grade: str      # e.g. "A+"
    passed: bool    # True if mark >= PASSING_MARK


# ─────────────────────────────────────────────────────────────────────────────
# DATACLASS  — auto-generates __init__, __repr__, __eq__
# Each field has a type annotation — mypy checks every assignment
# ─────────────────────────────────────────────────────────────────────────────

@dataclass
class Student:
    """Holds a student's personal info and their subject marks."""

    # Required fields (no default — must be passed to constructor)
    student_id: str         # unique identifier  e.g. "S001"
    name: str               # full name          e.g. "Alice Smith"

    # Optional fields (have defaults)
    # dict[str, int] → keys are subject names, values are marks 0–100
    marks: dict[str, int] = field(default_factory=dict)

    # ── computed property — not stored, calculated on the fly ──────────────

    @property
    def average(self) -> float:
        """Return the average mark across all subjects.
        Returns 0.0 if no subjects have been added yet.
        Type: float — mypy enforces that callers treat this as float.
        """
        if not self.marks:
            return 0.0
        # sum() and len() both return int; dividing gives float
        return sum(self.marks.values()) / len(self.marks)

    @property
    def is_passing(self) -> bool:
        """True if average mark is at or above PASSING_MARK.
        Type: bool — mypy catches if caller uses result as int by mistake.
        """
        return self.average >= PASSING_MARK

    def __str__(self) -> str:
        """Human-readable one-liner for a student.
        Return type -> str is enforced by mypy.
        """
        status = "PASS" if self.is_passing else "FAIL"
        return (
            f"[{self.student_id}] {self.name:<20} "
            f"| Avg: {self.average:5.1f} "
            f"| {status}"
        )


# ─────────────────────────────────────────────────────────────────────────────
# PURE FUNCTIONS with full type annotations
# These are stateless helpers — input → output, no side effects
# ─────────────────────────────────────────────────────────────────────────────

def calculate_grade(mark: int) -> Grade:
    """Convert a numeric mark to a Grade enum value.

    Args:
        mark: Integer between 0 and MAX_MARK inclusive.

    Returns:
        Grade enum — e.g. Grade.A_PLUS for mark=95.

    Raises:
        InvalidMarkError: If mark is outside 0–MAX_MARK.

    Type safety:
        - Parameter `mark` must be int (not float, not str)
        - Return type is Grade (enum), not a plain string
        - Mypy will error if caller ignores the return value's type
    """
    # Validate range before doing anything
    if not (0 <= mark <= MAX_MARK):
        raise InvalidMarkError(
            f"Mark {mark} is out of range. Must be 0–{MAX_MARK}."
        )

    # Match statement (Python 3.10+) — exhaustive, clean, type-safe
    # Ruff (UP) would warn if we used old-style if/elif chains unnecessarily
    if mark >= 90:
        return Grade.A_PLUS
    if mark >= 80:
        return Grade.A
    if mark >= 70:
        return Grade.B
    if mark >= 60:
        return Grade.C
    if mark >= 50:
        return Grade.D
    if mark >= 40:
        return Grade.E
    return Grade.F


def validate_mark(mark: int) -> None:
    """Raise InvalidMarkError if mark is not in 0–MAX_MARK.

    Return type is None — mypy checks we don't accidentally use
    the return value of this function.
    """
    if not (0 <= mark <= MAX_MARK):
        raise InvalidMarkError(
            f"Mark must be between 0 and {MAX_MARK}. Got: {mark}"
        )


def build_subject_result(subject: str, mark: int) -> SubjectResult:
    """Build a SubjectResult TypedDict from subject name and mark.

    Return type SubjectResult is a TypedDict — mypy verifies
    that all required keys are present and correctly typed.
    """
    validate_mark(mark)
    grade = calculate_grade(mark)

    # TypedDict constructor — mypy checks every key and value type
    return SubjectResult(
        subject=subject,
        mark=mark,
        grade=grade.value,      # .value converts Grade.A_PLUS → "A+"
        passed=mark >= PASSING_MARK,
    )


# ─────────────────────────────────────────────────────────────────────────────
# @overload — same function name, different return types based on argument
#
# Without @overload, get_summary("string") would return str | dict,
# and mypy would force you to check the type every time you use it.
# With @overload, mypy KNOWS exactly which type comes back.
# ─────────────────────────────────────────────────────────────────────────────

@overload
def get_summary(student: Student, fmt: Literal["string"]) -> str: ...

@overload
def get_summary(student: Student, fmt: Literal["dict"]) -> dict[str, object]: ...

def get_summary(
    student: Student,
    fmt: Literal["string", "dict"] = "string",
) -> str | dict[str, object]:
    """Return a student summary as either a string or a dictionary.

    The @overload decorators above tell mypy:
      - If fmt="string"  → return type is str
      - If fmt="dict"    → return type is dict[str, object]
    So callers never need to cast or check the type themselves.
    """
    results: list[SubjectResult] = [
        build_subject_result(subj, mark)
        for subj, mark in student.marks.items()
    ]

    if fmt == "dict":
        # Return structured dict — mypy knows this branch returns dict
        return {
            "student_id": student.student_id,
            "name":       student.name,
            "average":    round(student.average, 2),
            "is_passing": student.is_passing,
            "subjects":   results,         # list[SubjectResult]
        }

    # ── string branch ────────────────────────────────────────────────────────
    # Build a multi-line report string
    lines: list[str] = [
        f"\n{'─' * 45}",
        f"  Student : {student.name}  (ID: {student.student_id})",
        f"  Average : {student.average:.1f}",
        f"  Status  : {'✔ PASS' if student.is_passing else '✖ FAIL'}",
        f"{'─' * 45}",
    ]

    # Add one row per subject
    for result in results:
        status_icon = "✔" if result["passed"] else "✖"
        lines.append(
            f"  {status_icon} {result['subject']:<15} "
            f"Mark: {result['mark']:>3}   "
            f"Grade: {result['grade']}"
        )

    lines.append(f"{'─' * 45}")
    return "\n".join(lines)   # mypy knows this branch returns str


# ─────────────────────────────────────────────────────────────────────────────
# REGISTRY CLASS — manages a collection of students
# Uses Generic-style dict internally; all methods fully typed
# ─────────────────────────────────────────────────────────────────────────────

class StudentRegistry:
    """In-memory store for all students.

    Internally uses dict[str, Student]:
      - key   → student_id (str)
      - value → Student dataclass
    Mypy enforces correct key/value types throughout.
    """

    def __init__(self) -> None:
        # dict[str, Student] — mypy will catch if we try to store
        # anything other than Student values in this dict
        self._data: dict[str, Student] = {}

    # ── Add ───────────────────────────────────────────────────────────────────

    def add_student(self, student_id: str, name: str) -> Student:
        """Create and store a new student.

        Returns the created Student so callers can use it immediately.
        Raises DuplicateStudentError if ID already taken.
        """
        if student_id in self._data:
            raise DuplicateStudentError(
                f"Student ID '{student_id}' already exists."
            )
        # Create Student dataclass — mypy checks field types
        student = Student(student_id=student_id, name=name)
        self._data[student_id] = student
        return student

    # ── Get ───────────────────────────────────────────────────────────────────

    def get_student(self, student_id: str) -> Student:
        """Return a Student by ID.

        Return type is Student (not Student | None).
        We raise instead of returning None — cleaner for callers,
        and mypy does NOT force callers to null-check the result.
        """
        student = self._data.get(student_id)
        if student is None:
            raise StudentNotFoundError(
                f"No student with ID '{student_id}'."
            )
        return student

    # ── Add marks ─────────────────────────────────────────────────────────────

    def add_mark(
        self,
        student_id: str,
        subject: str,
        mark: int,
    ) -> None:
        """Add or update a subject mark for a student.

        Return type None — this is a mutation, not a query.
        Mypy will warn if a caller tries to use the return value.
        validate_mark() raises before any mutation happens.
        """
        validate_mark(mark)                     # raises if invalid
        student = self.get_student(student_id)  # raises if not found
        student.marks[subject] = mark           # dict[str, int] — type checked

    # ── List ──────────────────────────────────────────────────────────────────

    def all_students(self) -> list[Student]:
        """Return all students as a list.

        list[Student] — mypy knows every element is a Student,
        so callers can safely access .name, .average, etc.
        """
        return list(self._data.values())

    def passing_students(self) -> list[Student]:
        """Return only students whose average >= PASSING_MARK.

        list comprehension with type-safe filter — Ruff (C4) checks
        that we use comprehensions instead of map/filter where possible.
        """
        return [s for s in self._data.values() if s.is_passing]

    def failing_students(self) -> list[Student]:
        """Return only students who are failing."""
        return [s for s in self._data.values() if not s.is_passing]

    # ── Stats ─────────────────────────────────────────────────────────────────

    def class_average(self) -> float:
        """Return the average mark across ALL students.

        Returns 0.0 (float) when no students exist — consistent type,
        no need for Optional[float] which would burden callers.
        """
        students = self.all_students()
        if not students:
            return 0.0
        return sum(s.average for s in students) / len(students)

    def top_student(self) -> Student | None:
        """Return the student with the highest average, or None if empty.

        Return type Student | None — mypy forces every caller
        to handle the None case before using the result.
        """
        students = self.all_students()
        if not students:
            return None
        # max() with key= is a common pattern — Ruff won't complain
        return max(students, key=lambda s: s.average)

    def count(self) -> int:
        """Return the number of registered students."""
        return len(self._data)


# ─────────────────────────────────────────────────────────────────────────────
# DISPLAY HELPERS — thin presentation layer, no business logic
# All return None (they just print), annotated explicitly
# ─────────────────────────────────────────────────────────────────────────────

def print_header(title: str) -> None:
    """Print a section header."""
    print(f"\n{'═' * 50}")
    print(f"  {title}")
    print(f"{'═' * 50}")


def print_all_students(registry: StudentRegistry) -> None:
    """Print one-line summary for every student in the registry."""
    students = registry.all_students()
    if not students:
        print("  (no students yet)")
        return
    for student in students:
        # __str__ is defined on Student → returns str → safe to print
        print(f"  {student}")


def print_class_stats(registry: StudentRegistry) -> None:
    """Print aggregate statistics for the whole class."""
    print_header("Class Statistics")

    total: int    = registry.count()
    passing: int  = len(registry.passing_students())
    failing: int  = len(registry.failing_students())
    avg: float    = registry.class_average()

    # top_student() returns Student | None — we MUST handle None
    top: Student | None = registry.top_student()

    print(f"  Total students  : {total}")
    print(f"  Passing         : {passing}")
    print(f"  Failing         : {failing}")
    print(f"  Class average   : {avg:.1f}")

    # Mypy forces us to check `top is not None` before accessing `.name`
    if top is not None:
        print(f"  Top student     : {top.name} ({top.average:.1f})")
    else:
        print("  Top student     : N/A")


# ─────────────────────────────────────────────────────────────────────────────
# SEED DATA — populates the registry with demo students
# Uses explicit types to be clear about what we're building
# ─────────────────────────────────────────────────────────────────────────────

def seed_data(registry: StudentRegistry) -> None:
    """Add demo students and marks so the program starts with data.

    Parameter type: StudentRegistry — mypy ensures we don't
    accidentally pass a plain dict or wrong object here.
    """

    # list of tuples — each is (student_id, name, subject_marks)
    # Type: list[tuple[str, str, dict[str, int]]]
    demo: list[tuple[str, str, dict[str, int]]] = [
        ("S001", "Alice Smith",   {"Math": 92, "English": 88, "Science": 95}),
        ("S002", "Bob Jones",     {"Math": 45, "English": 38, "Science": 50}),
        ("S003", "Carol White",   {"Math": 76, "English": 82, "Science": 71}),
        ("S004", "David Brown",   {"Math": 55, "English": 60, "Science": 48}),
        ("S005", "Eva Green",     {"Math": 99, "English": 97, "Science": 100}),
        ("S006", "Frank Miller",  {"Math": 30, "English": 25, "Science": 20}),
    ]

    for student_id, name, subject_marks in demo:
        # add_student() returns Student — we use it immediately
        registry.add_student(student_id, name)
        for subject, mark in subject_marks.items():
            # add_mark() returns None — we don't capture it (Ruff B001)
            registry.add_mark(student_id, subject, mark)


# ─────────────────────────────────────────────────────────────────────────────
# MAIN PROGRAM — interactive menu loop
# Annotated as -> None because it runs forever until the user exits
# ─────────────────────────────────────────────────────────────────────────────

def show_menu() -> None:
    """Print the menu options."""
    print("\n┌─────────────────────────────────┐")
    print(f"│  {APP_TITLE:<31}│")
    print("├─────────────────────────────────┤")
    print("│  1. List all students           │")
    print("│  2. View student report         │")
    print("│  3. Add new student             │")
    print("│  4. Add mark to student         │")
    print("│  5. Show passing students       │")
    print("│  6. Show failing students       │")
    print("│  7. Class statistics            │")
    print("│  0. Exit                        │")
    print("└─────────────────────────────────┘")


def ask(prompt: str, default: str = "") -> str:
    """Prompt user, return stripped input or default if blank.

    Return type str — always returns a string, never None.
    Ruff (UP) ensures we use f-strings, not % formatting or .format().
    """
    suffix = f" [{default}]" if default else ""
    response = input(f"  {prompt}{suffix}: ").strip()
    return response if response else default


def safe_int(prompt: str) -> int | None:
    """Ask user for an integer, return None if they enter non-numeric input.

    Return type int | None — caller must handle both cases.
    This is safer than crashing on bad input.
    """
    raw = ask(prompt)
    if raw.isdigit():
        return int(raw)
    print(f"  ✖ '{raw}' is not a valid number.")
    return None


def run(registry: StudentRegistry) -> None:  # noqa: C901
    """Main interactive loop.

    Parameter type StudentRegistry — mypy checks we pass the right thing.
    Return type None — this function runs until sys.exit().
    noqa: C901 silences the 'too complex' warning for the long if/elif chain.
    """

    while True:
        show_menu()
        choice = ask("Choice")

        # ── Exit ─────────────────────────────────────────────────────────────
        if choice == "0":
            print("\n  Goodbye!\n")
            sys.exit(0)

        # ── List all students ─────────────────────────────────────────────────
        elif choice == "1":
            print_header("All Students")
            print_all_students(registry)

        # ── View student report ───────────────────────────────────────────────
        elif choice == "2":
            print_header("Student Report")
            sid = ask("Student ID")
            try:
                student = registry.get_student(sid)
                # get_summary with fmt="string" → mypy knows return is str
                report: str = get_summary(student, fmt="string")
                print(report)
            except StudentNotFoundError as exc:
                # exc is StudentNotFoundError — its message is a str
                print(f"  ✖ {exc}")

        # ── Add new student ───────────────────────────────────────────────────
        elif choice == "3":
            print_header("Add New Student")
            sid  = ask("Student ID (e.g. S007)")
            name = ask("Full Name")
            try:
                student = registry.add_student(sid, name)
                # student is Student — .name is str, guaranteed by dataclass
                print(f"  ✔ Added: {student.name} (ID: {student.student_id})")
            except DuplicateStudentError as exc:
                print(f"  ✖ {exc}")

        # ── Add mark ──────────────────────────────────────────────────────────
        elif choice == "4":
            print_header("Add Mark")
            sid     = ask("Student ID")
            subject = ask("Subject")

            # safe_int() returns int | None — we MUST check before using
            mark_input: int | None = safe_int("Mark (0–100)")
            if mark_input is None:
                continue   # skip rest of loop, go back to menu

            try:
                # At this point mypy knows mark_input is int (not None)
                registry.add_mark(sid, subject, mark_input)
                grade: Grade = calculate_grade(mark_input)
                print(
                    f"  ✔ Recorded {subject}: "
                    f"{mark_input}/100 → Grade {grade.value}"
                )
            except (StudentNotFoundError, InvalidMarkError) as exc:
                print(f"  ✖ {exc}")

        # ── Passing students ──────────────────────────────────────────────────
        elif choice == "5":
            print_header("Passing Students")
            # passing_students() returns list[Student] — fully typed
            passing: list[Student] = registry.passing_students()
            if not passing:
                print("  (none)")
            else:
                for s in passing:
                    print(f"  ✔ {s}")

        # ── Failing students ──────────────────────────────────────────────────
        elif choice == "6":
            print_header("Failing Students")
            # failing_students() returns list[Student] — same pattern
            failing: list[Student] = registry.failing_students()
            if not failing:
                print("  (none — everyone is passing!)")
            else:
                for s in failing:
                    print(f"  ✖ {s}")

        # ── Class statistics ──────────────────────────────────────────────────
        elif choice == "7":
            print_class_stats(registry)

        # ── Invalid choice ────────────────────────────────────────────────────
        else:
            print(f"  ✖ Invalid choice '{choice}' — try again.")


# ─────────────────────────────────────────────────────────────────────────────
# ENTRY POINT
# `if __name__ == "__main__"` ensures this only runs when executed directly,
# not when imported as a module.
# ─────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    # Create the registry — type: StudentRegistry
    registry = StudentRegistry()

    # Populate with demo data
    print(f"\n  Starting {APP_TITLE}…")
    seed_data(registry)
    print(f"  ✔ Loaded {registry.count()} students.")

    # Hand control to the interactive loop
    run(registry)
