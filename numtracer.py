def evenodd(num):
    if num % 2 == 0:
        return "Even"
    else:
        return "Odd"
def isprime(num):
    if num < 2:
        return False
    for i in range (2, int(num**0.5) + 1):
        if num % i == 0:
            return False
    return True
def factorial(num):
    if num == 0 or num == 1:
        return 1
    result = 1
    for i in range(2, num + 1):
        result *= i
    return result
def fib(n):
    series = []
    a, b = 0, 1
    for _ in range(n):
        series.append(a)
        a, b = b, a + b
    return series


num = int(input("Enter a number: "))

print(f"\n 1.{num} is {evenodd(num)}")
print(f"\n 2.{num} is {'Prime' if isprime(num) else 'Not Prime'}")
print(f"\n 3.{num}! = {factorial(num)}")
print(f"\n 4. Fibonacci series up to {num} terms: {fib(num)}")