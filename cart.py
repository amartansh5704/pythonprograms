cart = []

def add_item():
    name = input("Enter item name: ")
    price = float(input("Enter item price: "))
    qty = int(input("Enter item quantity: "))

    item = {"name": name, "price": price, "quantity": qty, "total": price * qty}
    cart.append(item)
    print(f"{name} added to cart.")

def view_cart():
    if len(cart) == 0:
        print("Your cart is empty.")
        return
    
    print("\n" + "=" * 55)
    print(f"{'Item':<15} {'Price':>8} {'Qty':>6} {'Total':>10}")
    print("=" * 55)

    grand_total = 0
    for item in cart:
        print(f"{item['name']:<15} ₹{item['price']:>7.2f} {item['quantity']:>6} ₹{item['total']:>9.2f}")
        grand_total += item["total"]

    print("=" * 55)
    print(f"{'GRAND TOTAL':>31} ₹{grand_total:>9.2f}")
    print("=" * 55)

while True:
    print("\n--- Shopping Cart Menu ---")
    print("1. Add Item")
    print("2. View Cart")
    print("3. Exit")

    choice = input("Enter your choice (1-3): ")
    if choice == "1":
        add_item()
    elif choice == "2":
        view_cart()
    elif choice == "3":
        print("Thank you for shopping with us!")
        break
    else:
        print("Invalid choice! Please select 1, 2, or 3.")