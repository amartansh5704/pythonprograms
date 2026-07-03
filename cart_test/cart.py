class ShoppingCart:

    def __init__(self):
        self.items = {}

    def add_item(self, name, price, quantity=1):
        if not isinstance(name, str) or name.strip() == "":
            raise ValueError("Item name must be a non-empty string")
        if price < 0:
            raise ValueError("Price cannot be negative")
        if quantity <= 0:
            raise ValueError("Quantity must be greater than zero")

        if name in self.items:
            self.items[name]["quantity"] += quantity
        else:
            self.items[name] = {"price": price, "quantity": quantity}

    def remove_item(self, name):
        if name not in self.items:
            raise KeyError(f"{name} is not in the cart")
        del self.items[name]

    def get_total(self):
        return sum(
            item["price"] * item["quantity"]
            for item in self.items.values()
        )

    def apply_discount(self, percent):
        if percent < 0 or percent > 100:
            raise ValueError("Discount must be between 0 and 100")
        discount = self.get_total() * (percent / 100)
        return self.get_total() - discount

    def get_item_count(self):
        return sum(item["quantity"] for item in self.items.values())

    def is_empty(self):
        return len(self.items) == 0

    def clear(self):
        self.items = {}