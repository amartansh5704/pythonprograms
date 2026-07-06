n = 10
a, b = 0, 1
print("Fibonacci Sequence:")
for i in range(n):
    print(a, end=" ")
    a, b = b, a+b

rows = 5
a, b = 0, 1
print("\nFibonacci Triangle:")
for i in range(rows):
    for j in range(i + 1):
        print(a, end=" ")
        a, b = b, a+b
    print()

n = 50
print("Prime Numbers:")
for num in range(2, n+1):
    for i in range(2, int(num**0.5) + 1):
        if num % i == 0:
            break
    else:
        print(num, end = " ")

rows = 5
primes = []
num = 2
while len(primes) < (rows*(rows + 1)) // 2:
    for i in range(2, int(num**0.5) + 1):
        if num % i == 0:
            break
    else:
        primes.append(num)
    num += 1

index = 0
print("\nPrime Pattern:")
for i in range(1, rows + 1):
    for j in range(i):
        print(primes[index], end = " ")
        index += 1
    print()


def factorial(n):
    if n == 0 or n == 1:
        return 1
    else:
        return n * factorial(n -1)

num = 10
print(f"\nFactorial of {num} is: {factorial(num)}")