from abc import ABC, abstractmethod
from datetime import datetime

class Person(ABC):
    
    total_persons = 0
    
    def __init__(self, name, age, email):
        self.name = name
        self.age = age
        self.__email = email
        self.join_date = datetime.now().strftime("%Y-%m-%d")
        Person.total_persons += 1
    
    @abstractmethod
    def get_role(self):
        pass
    
    @abstractmethod
    def display_info(self):
        pass
    
    def get_email(self):
        return self.__email
    
    def set_email(self, new_email):
        if "@" not in new_email:
            print(" Invalid email! Must contain @")
            return
        self.__email = new_email
        print(f" Email updated to {new_email}")
    
    def __str__(self):
        return f"{self.get_role()}: {self.name} (Age: {self.age})"


class Student(Person):
    
    def __init__(self, name, age, email, student_id, grade):
        super().__init__(name, age, email)
        self.student_id = student_id
        self.grade = grade
        self.__marks = {}
        self.attendance = 0
        self.total_days = 0
    
    def get_role(self):
        return "Student"
    
    def add_marks(self, subject, marks):
        if marks < 0 or marks > 100:
            print(f" Invalid marks! Must be between 0 and 100")
            return
        self.__marks[subject] = marks
        print(f" {self.name}: {subject} = {marks}/100")
    
    def get_average(self):
        if not self.__marks:
            return 0
        return sum(self.__marks.values()) / len(self.__marks)
    
    def get_grade_letter(self):
        avg = self.get_average()
        if avg >= 90: return "A+"
        elif avg >= 80: return "A"
        elif avg >= 70: return "B"
        elif avg >= 60: return "C"
        elif avg >= 50: return "D"
        else: return "F"
    
    def mark_attendance(self, present=True):
        self.total_days += 1
        if present:
            self.attendance += 1
    
    def get_attendance_percent(self):
        if self.total_days == 0:
            return 0
        return (self.attendance / self.total_days) * 100
    
    def display_info(self):
        print(f"\n{'='*50}")
        print(f"   STUDENT PROFILE")
        print(f"{'='*50}")
        print(f"  Name          : {self.name}")
        print(f"  Student ID    : {self.student_id}")
        print(f"  Age           : {self.age}")
        print(f"  Grade         : {self.grade}")
        print(f"  Email         : {self.get_email()}")
        print(f"  Joined        : {self.join_date}")
        print(f"\n   Academic Performance:")
        if self.__marks:
            for subject, mark in self.__marks.items():
                bar = "█" * (mark // 10) + "░" * (10 - mark // 10)
                print(f"    {subject:<15}: {bar} {mark}/100")
            print(f"    {'Average':<15}: {self.get_average():.1f} ({self.get_grade_letter()})")
        else:
            print("    No marks recorded yet")
        print(f"\n   Attendance: {self.attendance}/{self.total_days} days ({self.get_attendance_percent():.1f}%)")
        print(f"{'='*50}")


class Teacher(Person):
    
    def __init__(self, name, age, email, teacher_id, subject, salary):
        super().__init__(name, age, email)
        self.teacher_id = teacher_id
        self.subject = subject
        self.__salary = salary
        self.students = []
        self.experience_years = 0
    
    def get_role(self):
        return "Teacher"
    
    def get_salary(self):
        return self.__salary
    
    def give_raise(self, percent):
        if percent <= 0:
            print(" Raise percentage must be positive!")
            return
        raise_amount = self.__salary * (percent / 100)
        self.__salary += raise_amount
        print(f" {self.name} salary raised by {percent}%")
        print(f"   New salary: ₹{self.__salary:,.2f}")
    
    def assign_student(self, student):
        if student not in self.students:
            self.students.append(student)
            print(f" {student.name} assigned to {self.name}")
        else:
            print(f" {student.name} already assigned!")
    
    def grade_student(self, student, subject, marks):
        if student in self.students:
            student.add_marks(subject, marks)
        else:
            print(f" {student.name} is not your student!")
    
    def display_info(self):
        print(f"\n{'='*50}")
        print(f" TEACHER PROFILE")
        print(f"{'='*50}")
        print(f"  Name          : {self.name}")
        print(f"  Teacher ID    : {self.teacher_id}")
        print(f"  Age           : {self.age}")
        print(f"  Subject       : {self.subject}")
        print(f"  Email         : {self.get_email()}")
        print(f"  Salary        : ₹{self.__salary:,}")
        print(f"  Experience    : {self.experience_years} years")
        print(f"  Students      : {len(self.students)}")
        if self.students:
            print(f"  Student List  :")
            for s in self.students:
                print(f"    → {s.name} (Grade {s.grade})")
        print(f"{'='*50}")


class School:
    
    def __init__(self, school_name, location):
        self.school_name = school_name
        self.location = location
        self.__students = []
        self.__teachers = []
    
    def enroll_student(self, student):
        self.__students.append(student)
        print(f" {student.name} enrolled in {self.school_name}!")
    
    def hire_teacher(self, teacher):
        self.__teachers.append(teacher)
        print(f" {teacher.name} hired as {teacher.subject} teacher!")
    
    def get_topper(self):
        if not self.__students:
            return None
        return max(self.__students, key=lambda s: s.get_average())
    
    def get_all_students_report(self):
        print(f"\n ALL STUDENTS REPORT — {self.school_name}")
        print("=" * 60)
        print(f"{'Name':<20} {'Grade':<8} {'Average':<10} {'Letter':<8} {'Attendance'}")
        print("-" * 60)
        for student in self.__students:
            print(f"{student.name:<20} {student.grade:<8} {student.get_average():<10.1f} {student.get_grade_letter():<8} {student.get_attendance_percent():.1f}%")
        print("=" * 60)
    
    def school_summary(self):
        print(f"\n{'='*50}")
        print(f"   SCHOOL SUMMARY")
        print(f"{'='*50}")
        print(f"  School  : {self.school_name}")
        print(f"  Location: {self.location}")
        print(f"  Students: {len(self.__students)}")
        print(f"  Teachers: {len(self.__teachers)}")
        if self.__students:
            topper = self.get_topper()
            print(f"  Topper  : {topper.name} ({topper.get_average():.1f}%)")
        print(f"  Total People: {Person.total_persons}")
        print(f"{'='*50}")


print("=" * 50)
print("     SCHOOL MANAGEMENT SYSTEM")
print("=" * 50)

school = School("Python Public School", "Mumbai")

teacher1 = Teacher("Mrs. Sharma",  35, "sharma@school.com",  "TCH001", "Mathematics", 65000)
teacher2 = Teacher("Mr. Verma",    42, "verma@school.com",   "TCH002", "Science",     70000)

student1 = Student("Aarav Patel",  15, "aarav@email.com",  "STU001", "10th")
student2 = Student("Diya Sharma",  14, "diya@email.com",   "STU002", "9th")
student3 = Student("Rohan Gupta",  15, "rohan@email.com",  "STU003", "10th")

print("\n--- Hiring Teachers ---")
school.hire_teacher(teacher1)
school.hire_teacher(teacher2)

print("\n--- Enrolling Students ---")
school.enroll_student(student1)
school.enroll_student(student2)
school.enroll_student(student3)

print("\n--- Assigning Students to Teachers ---")
teacher1.assign_student(student1)
teacher1.assign_student(student3)
teacher2.assign_student(student2)

print("\n--- Recording Marks ---")
teacher1.grade_student(student1, "Mathematics", 92)
teacher1.grade_student(student1, "Science",     85)
teacher1.grade_student(student3, "Mathematics", 78)
teacher1.grade_student(student3, "Science",     82)
teacher2.grade_student(student2, "Mathematics", 88)
teacher2.grade_student(student2, "Science",     95)

print("\n--- Recording Attendance ---")
for _ in range(20):
    student1.mark_attendance(True)
    student2.mark_attendance(True)
for _ in range(3):
    student1.mark_attendance(False)
    student3.mark_attendance(True)

print("\n--- Displaying Profiles ---")
student1.display_info()
student2.display_info()
teacher1.display_info()

print()
school.get_all_students_report()
school.school_summary()

print("\n--- Testing Encapsulation ---")
student1.set_email("newemail@gmail.com")
teacher1.give_raise(10)

print("\n--- Polymorphism Demo ---")
all_persons = [teacher1, teacher2, student1, student2, student3]
for person in all_persons:
    print(f"Role: {person.get_role():<10} | {person}")