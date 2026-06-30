import json
import os

contact_file = "contacts.json"

def load_contacts():
    try:
        if os.path.exists(contact_file):
            with open(contact_file, "r") as f:
                return json.load(f)
        return []
    except json.JSONDecodeError:
        print("Error: contacts.json is not a valid JSON file.")
        return []
    
def save_contacts(contacts):
    try:
        with open(contact_file, "w") as f:
            json.dump(contacts, f, indent=4)
    except Exception as e:
        print(f"Error saving contacts: {e}")

def add_contact(contacts):
    name = input("Enter name: ")
    phone = input("Enter phone number: ")
    email = input("Enter email address: ")
    for c in contacts:
        if c["name"] == name:
            print(f"Contact with name {name} already exists.")
            return
    
    contacts.append({"name": name, "phone": phone, "email": email})
    save_contacts(contacts)
    print(f"Contact {name} added successfully!")

def view_contacts(contacts):
    if len(contacts) == 0:
        print("No contacts found.")
        return
    else:
        print("\nContacts List:")
        for c in contacts:
            print(f"Name: {c['name']}, Phone: {c['phone']}, Email: {c['email']}")

def search_contact(contacts):
    print("Search by:")
    keyword = input("Enter name, phone number, or email: ").strip().lower()
    results = []
    for c in contacts:
        if (keyword in c["name"].lower() or
            keyword in c["phone"].lower()):
            results.append(c)

    if len(results) == 0:
        print("No matching contacts found.")
    else:
        print("\nSearch Results:")
        for c in results:
            print(f"Name: {c['name']}, Phone: {c['phone']}, Email: {c['email']}")

def delete_contact(contacts):
    name = input("Enter the name of the contact to delete: ")
    for c in contacts:
        if c["name"] == name:
            contacts.remove(c)
            save_contacts(contacts)
            print(f"Contact {name} deleted successfully!")
            return
    print(f"No contact found with name {name}.")

def update_contact(contacts):
    name = input("Enter the name of the contact to update: ").strip().lower()

    for c in contacts:
        if c["name"].lower() == name:
            print(f"Editing contact {c['name']} | Phone: {c['phone']}, Email: {c['email']}")
            print("Press Enter to keep the current value.")

            new_name = input(f"Enter new name (current: {c['name']}): ").strip()
            new_phone = input(f"Enter new phone number (current: {c['phone']}): ").strip()
            new_email = input(f"Enter new email address (current: {c['email']}): ").strip()

        if new_name: 
            c["name"] = new_name
        if new_phone:
            c["phone"] = new_phone
        if new_email:
            c["email"] = new_email
        save_contacts(contacts)
        print(f"Contact {c['name']} updated successfully!")
        return
def main():
    contacts = load_contacts()

    while True:
        print("\n--- Contact Manager ---")
        print("1. Add Contact")
        print("2. View Contacts")
        print("3. Search Contact")
        print("4. Update Contact")
        print("5. Delete Contact")
        print("6. Exit")

        try:
            choice = input("Enter your choice (1-6): ")
            if choice == "1":
                add_contact(contacts)
            elif choice == "2":
                view_contacts(contacts)
            elif choice == "3":
                search_contact(contacts)
            elif choice == "4":
                update_contact(contacts)
            elif choice == "5":
                delete_contact(contacts)
            elif choice == "6":
                print("Exiting the program.")
                break
            else:
                print("Invalid choice! Please select a number between 1 and 6.")
        except KeyboardInterrupt:
            print("\nProgram interrupted by user.")
            break
        
main()