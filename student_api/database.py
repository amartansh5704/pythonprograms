# database.py
import json
import os

DATABASE_FILE = "students.json"

# ── LOCK to prevent multiple simultaneous writes ──────────────
import threading
db_lock = threading.Lock()
# This lock makes sure only ONE write happens at a time
# If two requests come in simultaneously, second one WAITS


def read_database():
    """Read all data from JSON file"""

    if not os.path.exists(DATABASE_FILE):
        empty_data = {
            "students": [],
            "next_id": 1
        }
        write_database(empty_data)
        return empty_data

    with open(DATABASE_FILE, "r") as file:
        data = json.load(file)

    return data


def write_database(data: dict):
    """Write data to JSON file"""

    with open(DATABASE_FILE, "w") as file:
        json.dump(data, file, indent=2)


def get_all_students():
    """Get all students"""
    data = read_database()
    return data["students"]


def get_student_by_id(student_id: int):
    """Get one student by ID"""
    students = get_all_students()
    for student in students:
        if student["id"] == student_id:
            return student
    return None


def save_student(student_data: dict):
    """
    Save a new student.
    Uses a LOCK so two requests cant write at the same time.
    Also checks for duplicate email before saving.
    """

    # Lock means: only one thread can be inside here at a time
    # Second request WAITS until first one finishes
    with db_lock:

        # Read INSIDE the lock (fresh read)
        data = read_database()

        # Double-check email duplicate INSIDE the lock
        # (Frontend checks too, but this is the safety net)
        for existing in data["students"]:
            if existing["email"] == student_data.get("email", "").lower():
                return None  # Signal that email already exists

        # Assign ID
        student_data["id"] = data["next_id"]

        # Add to list
        data["students"].append(student_data)

        # Increment next ID
        data["next_id"] += 1

        # Write to file
        write_database(data)

        # Return the saved student
        return student_data


def update_student(student_id: int, updated_data: dict):
    """Update a student"""

    with db_lock:
        data = read_database()

        for index, student in enumerate(data["students"]):
            if student["id"] == student_id:
                data["students"][index].update(updated_data)
                data["students"][index]["id"] = student_id
                write_database(data)
                return data["students"][index]

    return None


def delete_student(student_id: int):
    """Delete a student"""

    with db_lock:
        data = read_database()
        original_count = len(data["students"])

        data["students"] = [
            s for s in data["students"]
            if s["id"] != student_id
        ]

        if len(data["students"]) == original_count:
            return False

        write_database(data)
        return True


def search_students(keyword: str):
    """Search students by name or subject"""

    students = get_all_students()
    keyword_lower = keyword.lower()

    results = [
        student for student in students
        if keyword_lower in student["name"].lower()
        or keyword_lower in student["subject"].lower()
    ]

    return results