print("Choose a pattern to print:")
print("1. Right Triangle")
print("2. Inverted Triangle")
print("3. Pyramid")
print("4. Reverse Pyramid")
print("5. Inverted Right Triangle")
print("6. Diamond")

choice = int(input("Enter your choice (1/2/3/4/5/6): "))
rows = int(input("Enter the number of rows: "))
print()

if choice == 1:
    print("Right Triangle Pattern:")
    for i in range (1, rows+1):
        print ("*" * i)

elif choice == 2:
    print ("Inverted Triangle Pattern:")
    for i in range(rows,0,-1):
        print("*" * i)

elif choice == 3:
    print("Pyramid Pattern:")
    for i in range(1, rows + 1):
        spaces = ' '*(rows - i)
        stars = '*'* (2 * i - 1)
        print(spaces + stars)

elif choice == 4:
    print("Reverse Pyramid Pattern: ")
    for i in range (rows, 0, -1):
        spaces = ' ' * (rows - i)
        stars = '*' * (2*i - 1)
        print(spaces + stars)

elif choice == 5:
    print("Inverted Right Triangle: ")
    for i in range (rows, 0, -1):
        print ("*" * i)


elif choice == 6:
    print("Diamond")
    for i in range (1, rows+1):
        spaces = ' ' * (rows-i)
        stars = '*' * (2*i - 1)
        print(spaces+stars)

    for i in range (rows-1, 0, -1):
        spaces = ' ' * (rows-i)
        stars = "*" * (2*i -1)
        print(spaces+stars)


else:
    print("Invalid choice! Please select 1, 2, 3,4,5 or 6.")
