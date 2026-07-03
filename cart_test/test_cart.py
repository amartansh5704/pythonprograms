import unittest
from cart import ShoppingCart


class TestShoppingCartAddItem(unittest.TestCase):

    def setUp(self):
        self.cart = ShoppingCart()

    def test_add_single_item(self):
        self.cart.add_item("apple", 1.50)
        self.assertIn("apple", self.cart.items)

    def test_add_item_stores_price(self):
        self.cart.add_item("apple", 1.50)
        self.assertEqual(self.cart.items["apple"]["price"], 1.50)

    def test_add_item_default_quantity(self):
        self.cart.add_item("apple", 1.50)
        self.assertEqual(self.cart.items["apple"]["quantity"], 1)

    def test_add_item_custom_quantity(self):
        self.cart.add_item("apple", 1.50, quantity=3)
        self.assertEqual(self.cart.items["apple"]["quantity"], 3)

    def test_add_same_item_twice_increases_quantity(self):
        self.cart.add_item("apple", 1.50, quantity=2)
        self.cart.add_item("apple", 1.50, quantity=3)
        self.assertEqual(self.cart.items["apple"]["quantity"], 5)

    def test_add_item_negative_price_raises_error(self):
        with self.assertRaises(ValueError):
            self.cart.add_item("apple", -1.00)

    def test_add_item_zero_quantity_raises_error(self):
        with self.assertRaises(ValueError):
            self.cart.add_item("apple", 1.50, quantity=0)

    def test_add_item_empty_name_raises_error(self):
        with self.assertRaises(ValueError):
            self.cart.add_item("", 1.50)


class TestShoppingCartRemoveItem(unittest.TestCase):

    def setUp(self):
        self.cart = ShoppingCart()
        self.cart.add_item("apple", 1.50)
        self.cart.add_item("banana", 0.75)

    def test_remove_existing_item(self):
        self.cart.remove_item("apple")
        self.assertNotIn("apple", self.cart.items)

    def test_remove_item_leaves_others(self):
        self.cart.remove_item("apple")
        self.assertIn("banana", self.cart.items)

    def test_remove_nonexistent_item_raises_error(self):
        with self.assertRaises(KeyError):
            self.cart.remove_item("mango")


class TestShoppingCartTotal(unittest.TestCase):

    def setUp(self):
        self.cart = ShoppingCart()

    def test_empty_cart_total(self):
        self.assertEqual(self.cart.get_total(), 0)

    def test_single_item_total(self):
        self.cart.add_item("apple", 2.00)
        self.assertEqual(self.cart.get_total(), 2.00)

    def test_multiple_items_total(self):
        self.cart.add_item("apple", 2.00)
        self.cart.add_item("banana", 1.00)
        self.assertEqual(self.cart.get_total(), 3.00)

    def test_total_with_quantity(self):
        self.cart.add_item("apple", 2.00, quantity=3)
        self.assertEqual(self.cart.get_total(), 6.00)


class TestShoppingCartDiscount(unittest.TestCase):

    def setUp(self):
        self.cart = ShoppingCart()
        self.cart.add_item("laptop", 1000.00)

    def test_ten_percent_discount(self):
        self.assertEqual(self.cart.apply_discount(10), 900.00)

    def test_zero_discount(self):
        self.assertEqual(self.cart.apply_discount(0), 1000.00)

    def test_hundred_percent_discount(self):
        self.assertEqual(self.cart.apply_discount(100), 0.00)

    def test_discount_above_100_raises_error(self):
        with self.assertRaises(ValueError):
            self.cart.apply_discount(110)

    def test_negative_discount_raises_error(self):
        with self.assertRaises(ValueError):
            self.cart.apply_discount(-10)


class TestShoppingCartOther(unittest.TestCase):

    def setUp(self):
        self.cart = ShoppingCart()

    def test_empty_cart_is_empty(self):
        self.assertTrue(self.cart.is_empty())

    def test_cart_not_empty_after_adding(self):
        self.cart.add_item("apple", 1.00)
        self.assertFalse(self.cart.is_empty())

    def test_item_count(self):
        self.cart.add_item("apple", 1.00, quantity=2)
        self.cart.add_item("banana", 0.50, quantity=3)
        self.assertEqual(self.cart.get_item_count(), 5)

    def test_clear_empties_cart(self):
        self.cart.add_item("apple", 1.00)
        self.cart.clear()
        self.assertTrue(self.cart.is_empty())


if __name__ == "__main__":
    unittest.main()