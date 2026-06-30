def safe_divide():
    print(f"Dividing two numbers:")
    try:
        a = float(input("Enter the numerator:"))
        b = float(input("Enter the denominator:"))
        result = a / b
        print(f"The result of {a} divided by {b} is: {result}")
    except ValueError:
        print("Please enter valid numbers.")
    except ZeroDivisionError:
        print("Denominator cannot be zero.")

def safe_file_read():
    print(f"Reading a file safely:")
    filename = input("Enter the filename to read:")
    try:
        with open(filename, 'r') as file:
            content = file.read()
            print (f"Content of the file '{filename}':\n{content}")
    except FileNotFoundError:
        print(f"The file '{filename}' does not exist.")
    except PermissionError:
        print(f"You do not have permission to read the file '{filename}'.")
    finally:
        print("File read operation completed.")

def safe_list_access():
    print(f"Accessing a list safely:")
    my_list = [10,20,30,40,50]
    print(f"Current list: {my_list}")
    try:
        index = int(input("Enter the index of the element you want to access:"))
        print(f"The element at index {index} is: {my_list[index]}")
    except IndexError:
        print(f"Index {index} is out of range. Please enter a valid index between 0 and {len(my_list)-1}.")
    except ValueError:
        print("Please enter a valid integer index.")
    finally:
        print("List access operation completed.")

def custom_exception_demo():
    print(f"Demonstrating custom exception:")
    try:
        age = int(input("Enter your age:"))
        if age < 0:
            raise ValueError("Age cannot be negative.")
        if age > 120:
            raise ValueError("Age seems fake.")
        print(f"Your age is: {age}")
    except ValueError as ve:
        print(f"Error: {ve}")
    finally:
        print("Age input operation completed.")

while True:
    print("\n--- Exception Handling Demonstration ---")
    print("1. Safe Division")
    print("2. Safe File Read")
    print("3. Safe List Access")
    print("4. Custom Exception Demo")
    print("5. Exit")
    
    choice = input("Enter your choice (1-5): ")
    
    if choice == '1':
        safe_divide()
    elif choice == '2':
        safe_file_read()
    elif choice == '3':
        safe_list_access()
    elif choice == '4':
        custom_exception_demo()
    elif choice == '5':
        print("Exiting the program.")
        break
    else:
        print("Invalid choice! Please select a valid option.")