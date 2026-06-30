students = []
marks = []

def add_student():
    name = input("Enter student name  : ")
    mark = float(input(f"Enter marks for {name}: "))
    students.append(name)
    marks.append(mark)
    print(f"{name} added successfully!\n")

def show_all():
    if len(students) == 0:
        print("No students added yet!")
        return
    print("\n" + "=" * 40)
    print(f"{'Name':<20} {'Marks':<10} {'Grade'}")
    print("=" * 40)
    for i in range(len(students)):
        grade = get_grade(marks[i])
        print(f"{students[i]:<20} {marks[i]:<10} {grade}")
    print("=" * 40)

def get_grade(mark):
    if mark >= 90:
        return "A+"
    elif mark >= 80:
        return "A"
    elif mark >= 70:
        return "B"
    elif mark >= 60:
        return "C"
    else:
        return "F"

def show_stats():
    if len(marks) == 0:
        print("No data available!")
        return
    print(f"\n Total Students : {len(students)}")
    print(f" Highest Marks  : {max(marks)} — {students[marks.index(max(marks))]}")
    print(f" Lowest Marks   : {min(marks)} — {students[marks.index(min(marks))]}")
    print(f" Average Marks  : {sum(marks)/len(marks):.2f}")


while True:
    print("\n--- STUDENT MARKS MANAGER ---")
    print("1. Add Student")
    print("2. Show All Students")
    print("3. Show Statistics")
    print("4. Exit")

    choice = input("\nEnter choice: ")

    if choice == "1":
        add_student()
    elif choice == "2":
        show_all()
    elif choice == "3":
        show_stats()
    elif choice == "4":
        print("Goodbye!")
        break
    else:
        print("Invalid choice! Try again.")