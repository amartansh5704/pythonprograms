#multiplication table
num = int(input("Enter a number:"))
print(f"\nMultiplication table of {num}:")
print("-" * 30)
for i in range(1, 11):
    result = num * i
    print(f"{num} x {i} = {result}")
    