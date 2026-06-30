def add(a,b):
    return a+b

def subtract(a,b):
    return a-b

def multiply(a,b):
    return a*b

def divide(a,b):
    if b == 0:
        return "Error: Division by zero is not allowed."
    return a/b

def calculator():
    print("="*30)
    print("Simple Calculator")
    print("="*30)

    num1 = float(input("First number: "))
    num2 = float(input("Second number: "))
    op = input("Enter operation (+, -, *, /): ")

    if op == '+':
        result = add(num1,num2)
    elif op == '-':
        result = subtract(num1,num2)
    elif op == '*':
        result = multiply(num1,num2)
    elif op == '/':
        result = divide(num1,num2)
    else:
        print("Invalid operation! Please select +, -, *, or /.")
        return
    print(f"Result: {result}")
calculator()