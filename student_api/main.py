from fastapi import FastAPI, HTTPException, status, Query
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional
import os
from database import(get_all_students, get_student_by_id, save_student, update_student, delete_student, search_students)
from models import (Student_Create, Student_Update, Student_Response, Message_Response)




app = FastAPI(title="Student API", description="A simple API for managing students", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

os.makedirs("static", exist_ok=True)
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", include_in_schema=False)
def serve_frontend():
    return FileResponse("static/index.html")


@app.get("/students", response_model = List[Student_Response], status_code=status.HTTP_200_OK, tags=["Students"], summary= "Get all students")
def get_students(
    enrolled: Optional[bool] = Query(None, description="Filter by enrollment status"),
    grade: Optional[str] = Query(None, description="Filter by grade (A, B, C, D, F)"),
    subject: Optional[str] = Query(None, description="Filter by subject")
):
    students = get_all_students()
    if enrolled is not None:
        students = [s for s in students if s["enrolled"] == enrolled]
    
    if grade is not None:
        grade_upper = grade.upper()
        students = [s for s in students if s["grade"] == grade_upper]

    if subject is not None:
        subject_lower = subject.lower()
        students = [s for s in students if subject_lower in s["subject"].lower()]

    return students

@app.get("/students/search", response_model=List[Student_Response], status_code=status.HTTP_200_OK, tags=["Students"], summary="Search students by keyword")
def search( q: str = Query(..., description="Keyword to search in name or subject")):
    results = search_students(q)
    return results

@app.get("/students/{student_id}", response_model=Student_Response, status_code=status.HTTP_200_OK, tags=["Students"], summary="Get a student by ID")
def get_student(student_id: int):
    student = get_student_by_id(student_id)
    if student is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Student with ID {student_id} not found")
    return student

@app.post(
    "/students",
    response_model=Student_Response,
    status_code=status.HTTP_201_CREATED,
    tags=["Students"]
)
def create_student(student: Student_Create):

    # Check email duplicate BEFORE saving
    all_students = get_all_students()
    for existing in all_students:
        if existing["email"] == student.email.lower():
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Email '{student.email}' is already registered"
            )

    student_dict = student.model_dump()

    # save_student returns None if email already exists (double safety)
    saved = save_student(student_dict)

    if saved is None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Email '{student.email}' is already registered"
        )

    return saved

@app.put("/students/{student_id}", response_model=Student_Response, status_code=status.HTTP_200_OK, tags=["Students"], summary="Update a student by ID")
def update_student_endpoint(student_id: int, student_update: Student_Update):
    existing = get_student_by_id(student_id)
    if existing is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Student with ID {student_id} not found")
    
    updated_data = student_update.model_dump(exclude_unset=True)

    if not updated_data:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No fields provided for update")
    
    if "email" in updated_data:
        all_students = get_all_students()
        for s in all_students:
            if s["id"] == student_id:
                continue
            if s["email"] == updated_data["email"]:
                raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already exists")
    updated_student = update_student(student_id, updated_data)
    return updated_student

@app.delete("/students/{student_id}", response_model=Message_Response, status_code=status.HTTP_200_OK, tags=["Students"], summary="Delete a student by ID")
def delete_student_endpoint(student_id: int):
    deleted = delete_student(student_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Student with ID {student_id} not found")
    return {"message": f"Student with ID {student_id} deleted successfully", "success": True}

@app.get("/stats", response_model=dict, status_code=status.HTTP_200_OK, tags=["Statistics"], summary="Get statistics about students")
def get_stats():
    students = get_all_students()

    if not students:
        return {
            "total_students": 0,
            "enrolled": 0,
            "not_enrolled": 0,
            "grades": {},
            "subjects": {}
        }
    enrolled_count = sum(1 for s in students if s["enrolled"])
    not_enrolled_count = len(students) - enrolled_count

    grade_counts = {}
    for student in students:
        grade = student["grade"]
        if grade not in grade_counts:
            grade_counts[grade] = 0
        grade_counts[grade] += 1

    unique_subjects = set(student["subject"] for student in students)

    return {
        "total_students": len(students),
        "enrolled": enrolled_count,
        "not_enrolled": not_enrolled_count,
        "grades": grade_counts,
        "subjects": unique_subjects
    }

