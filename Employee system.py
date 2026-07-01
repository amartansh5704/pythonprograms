class Employee:
    company_name = "Tecorp"

    def __init__(self, name, employee_id, department, salary):
        self.name = name
        self.employee_id = employee_id
        self.department = department
        self.salary = salary
        self.isActive = True

    def display_info(self):
        print("=" * 30)
        print(f"Company: {self.company_name}")
        print("=" * 30)        
        print(f"Employee Name: {self.name}")
        print(f"Employee ID: {self.employee_id}")
        print(f"Department: {self.department}")
        print(f"Salary: ${self.salary}")
        print(f"Active Status: {'Active' if self.isActive else 'Inactive'}")
        print("=" * 30)

    def calculate_bonus(self):
        bonus = self.salary*0.10
        return bonus
    def give_raise(self, percentage):
        raise_amount = self.salary * (percentage / 100)
        self.salary += raise_amount
        print(f"{self.name} has received a raise of {percentage}%. New salary: ${self.salary}")
    def deactivate(self):
        self.isActive = False
        print(f"{self.name} has been deactivated from the company.")
    def __str__ (self):
        return f"Employee(Name: {self.name}, ID: {self.employee_id}, Department: {self.department})"

class Manager(Employee):
    def __init__(self, name, employee_id, department, salary, team_size):
        super().__init__(name, employee_id, department, salary)
        self.team_size = team_size
        self.team_members = []
    def add_team_member(self, employee):
        self.team_members.append(employee)
        print(f"{employee.name} has been added to {self.name}'s team.")
    def display_info(self):
        super().display_info()
        print(f"Team Size: {self.team_size}")
        print(f"Team Members: {[e.name for e in self.team_members]}")
        print("=" * 30)
    def calculate_bonus(self):
        bonus = self.salary * 0.15 
        return bonus
    def show_team(self):
        if len(self.team_members) == 0:
            print(f"{self.name} has no team members.")
            return
        print(f"Team Members of {self.name}:")
        print("=" * 30)
        for i, member in enumerate(self.team_members, start=1):
            print(f"{i}. {member.name} Department: {member.department}")
        print("=" * 30)
    
class Intern(Employee):
    def __init__(self, name, employee_id, department, salary, duration):
        super().__init__(name, employee_id, department, salary)
        self.duration = duration
        self.is_Intern = True
    def display_info(self):
        super().display_info()
        print(f"Internship Duration: {self.duration} months")
        print("=" * 30)
    def calculate_bonus(self):
        bonus = self.salary * 0.05 
        return bonus
    def convert_to_fulltime(self, new_salary):
        self.salary = new_salary
        self.is_Intern = False
        print(f"{self.name} has been converted to a full-time employee with a salary of ${self.salary}.")

print("Welcome to the Employee Management System")

manager1 = Manager("Alice Johnson", "M001", "Engineering", 90000, 5)
employee1 = Employee("Bob Smith", "E001", "Engineering", 60000)
employee2 = Employee("Charlie Brown", "E002", "Engineering", 65000)
intern1 = Intern("David Lee", "I001", "Engineering", 30000, 6)

print ("\nDisplaying Manager Information:")
manager1.display_info()
employee1.display_info()
employee2.display_info()
intern1.display_info()

print ("Calculating Bonuses:")
print(f"{manager1.name}'s Bonus: ${manager1.calculate_bonus()}")
print(f"{employee1.name}'s Bonus: ${employee1.calculate_bonus()}")
print(f"{employee2.name}'s Bonus: ${employee2.calculate_bonus()}")
print(f"{intern1.name}'s Bonus: ${intern1.calculate_bonus()}")

print()
manager1.add_team_member(employee1)
manager1.add_team_member(employee2)
manager1.add_team_member(intern1)
manager1.show_team()

print()
employee1.give_raise(10)

print()
intern1.convert_to_fulltime(40000)

print()
print(manager1)
print(employee1)
print(employee2)
print(intern1)