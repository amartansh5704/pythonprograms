from pydantic import BaseModel, Field, field_validator
from typing import Optional

class Student_Create(BaseModel):

    name: str = Field(..., min_length=2, max_length=50, description="The name of the student", example="John Doe")
    age: int = Field(..., ge = 5, le = 100, description="The age of the student", example=20)
    grade: str = Field(..., description="A, B, C, D, or F", example="A")
    subject: str = Field(..., min_length=2, max_length=50, description="The subject the student is studying", example="Mathematics")
    email: str = Field(..., description="The email address of the student", example="school@gmail.com")
    enrolled: bool = Field(default=True, description="Whether the student is currently enrolled")

    @field_validator("grade")
    def grade_must_be_valid(cls, v):
        v = v.upper()
        valid_grades = {"A", "B", "C", "D", "F"}
        if v not in valid_grades:
            raise ValueError("Grade must be one of A, B, C, D, or F")
        return v
    
    @field_validator("email")
    def email_must_be_valid(cls, v):
        if '@' not in v:
            raise ValueError("Email must contain '@'")
        return v.lower()
    
class Student_Update(BaseModel):
    name: Optional[str] = Field(None, min_length=2, max_length=50)
    age: Optional[int] = Field(None, ge=5, le=100)
    grade: Optional[str] = None
    subject: Optional[str] = Field(None, min_length=2, max_length=50)
    email: Optional[str] = None
    enrolled: Optional[bool] = None

    @field_validator("grade")
    def grade_must_be_valid(cls, v):
        if v is not None:
            return v
        v = v.upper()
        valid_grades = {"A", "B", "C", "D", "F"}
        if v not in valid_grades:
            raise ValueError("Grade must be one of A, B, C, D, or F")
        return v
    
class Student_Response(BaseModel):
    id: int
    name: str
    age: int
    grade: str
    subject: str
    email: str
    enrolled: bool

class Message_Response(BaseModel):
    message: str
    success: bool

