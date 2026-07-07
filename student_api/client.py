# client.py
# This file shows how to INTERACT with our API
# Run this AFTER starting the API server

import requests
import json

# Base URL of our API
BASE_URL = "http://127.0.0.1:8000"


def print_response(response, title=""):
    """Helper function to print responses nicely"""
    print(f"\n{'='*50}")
    if title:
        print(f"  {title}")
    print(f"  Status Code: {response.status_code}")
    print(f"  Response:")
    
    # Pretty print the JSON response
    try:
        print(json.dumps(response.json(), indent=4))
    except:
        print(response.text)
    print('='*50)


# ── TEST 1: CHECK API IS RUNNING ───────────────────────────
def test_root():
    print("\n🔵 Testing: API Health Check")
    
    response = requests.get(f"{BASE_URL}/")
    print_response(response, "Root Endpoint")


# ── TEST 2: GET ALL STUDENTS ───────────────────────────────
def test_get_all_students():
    print("\n🔵 Testing: Get All Students")
    
    response = requests.get(f"{BASE_URL}/students")
    print_response(response, "All Students")


# ── TEST 3: GET STUDENTS WITH FILTER ──────────────────────
def test_get_students_filtered():
    print("\n🔵 Testing: Get Only Enrolled Students")
    
    # Add query parameter to filter
    response = requests.get(
        f"{BASE_URL}/students",
        params={"enrolled": True}   # ?enrolled=true
    )
    print_response(response, "Enrolled Students Only")
    
    print("\n🔵 Testing: Get Students with Grade A")
    response = requests.get(
        f"{BASE_URL}/students",
        params={"grade": "A"}       # ?grade=A
    )
    print_response(response, "Grade A Students")


# ── TEST 4: GET ONE STUDENT ────────────────────────────────
def test_get_one_student():
    print("\n🔵 Testing: Get Student by ID")
    
    # Get student with ID 1
    response = requests.get(f"{BASE_URL}/students/1")
    print_response(response, "Student ID 1")
    
    # Try to get non-existent student
    print("\n🔵 Testing: Get Non-existent Student (should be 404)")
    response = requests.get(f"{BASE_URL}/students/9999")
    print_response(response, "Student ID 9999 (should fail)")


# ── TEST 5: CREATE NEW STUDENT ─────────────────────────────
def test_create_student():
    print("\n🔵 Testing: Create New Student")
    
    # Data for new student
    new_student = {
        "name": "David Brown",
        "age": 23,
        "grade": "B",
        "subject": "Biology",
        "email": "david@school.com",
        "enrolled": True
    }
    
    response = requests.post(
        f"{BASE_URL}/students",
        json=new_student            # json= sets Content-Type automatically
    )
    print_response(response, "Created Student")
    
    # Try to create duplicate email (should fail)
    print("\n🔵 Testing: Create Student with Duplicate Email (should fail)")
    response = requests.post(
        f"{BASE_URL}/students",
        json=new_student  # Same email - should get 409 conflict
    )
    print_response(response, "Duplicate Email (should fail)")


# ── TEST 6: UPDATE STUDENT ─────────────────────────────────
def test_update_student():
    print("\n🔵 Testing: Update Student")
    
    # Update only the grade of student 1
    update_data = {
        "grade": "A",       # Only updating grade
        "enrolled": True    # And enrollment status
    }
    
    response = requests.put(
        f"{BASE_URL}/students/1",
        json=update_data
    )
    print_response(response, "Updated Student 1")


# ── TEST 7: SEARCH STUDENTS ────────────────────────────────
def test_search():
    print("\n🔵 Testing: Search Students")
    
    # Search for "alice"
    response = requests.get(
        f"{BASE_URL}/students/search",
        params={"q": "alice"}       # ?q=alice
    )
    print_response(response, "Search: 'alice'")
    
    # Search by subject
    response = requests.get(
        f"{BASE_URL}/students/search",
        params={"q": "math"}
    )
    print_response(response, "Search: 'math'")


# ── TEST 8: GET STATS ──────────────────────────────────────
def test_stats():
    print("\n🔵 Testing: Get Statistics")
    
    response = requests.get(f"{BASE_URL}/stats")
    print_response(response, "Database Statistics")


# ── TEST 9: DELETE STUDENT ─────────────────────────────────
def test_delete_student():
    print("\n🔵 Testing: Delete Student")
    
    # Delete student with ID 3
    response = requests.delete(f"{BASE_URL}/students/3")
    print_response(response, "Delete Student 3")
    
    # Try to delete again (should fail)
    print("\n🔵 Testing: Delete Already Deleted Student (should fail)")
    response = requests.delete(f"{BASE_URL}/students/3")
    print_response(response, "Delete Student 3 Again (should fail)")


# ── RUN ALL TESTS ──────────────────────────────────────────
if __name__ == "__main__":
    print("🚀 Starting API Tests")
    print("Make sure the server is running: uvicorn main:app --reload")
    print("="*60)
    
    test_root()
    test_get_all_students()
    test_get_students_filtered()
    test_get_one_student()
    test_create_student()
    test_update_student()
    test_search()
    test_stats()
    test_delete_student()
    
    print("\n✅ All tests completed!")