import datetime
diary_file = "diary.txt"

def write_entry():
    entry = input(" Write your diary entry:\n> ")
    today = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open(diary_file, "a") as file:
        file.write(f"\n{'='*50}\n")
        file.write(f"Date & Time: {today}\n")
        file.write(f"{entry}\n")
    
def read_entries():
    try:
        with open(diary_file, "r") as file:
            content = file.read()
            if content.strip() == "":
                print ("No diary entries found.")
            else:
                print("\n--- Diary Entries ---")
                print(content)
    except FileNotFoundError:
        print("No diary entries found.")

while True:
    print("\n--- Diary Menu ---")
    print("1. Write a new entry")
    print("2. Read all entries")
    print("3. Exit")

    choice = input("Enter your choice (1-3): ")
    if choice == "1":
        write_entry()
    elif choice == "2":
        read_entries()
    elif choice == "3":
        print("Goodbye!")
        break
    else:
        print("Invalid choice! Please select 1, 2, or 3.")