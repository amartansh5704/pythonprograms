import unittest
from math_utils import factorial, is_prime, fibonacci, clamp, is_even, power


class TestFactorial(unittest.TestCase):

    def test_zero(self):
        self.assertEqual(factorial(0), 1)

    def test_one(self):
        self.assertEqual(factorial(1), 1)

    def test_positive_number(self):
        self.assertEqual(factorial(5), 120)

    def test_large_number(self):
        self.assertEqual(factorial(10), 3628800)

    def test_negative_raises_value_error(self):
        with self.assertRaises(ValueError):
            factorial(-1)

    def test_float_raises_type_error(self):
        with self.assertRaises(TypeError):
            factorial(3.5)


class TestIsPrime(unittest.TestCase):

    def test_prime_number(self):
        self.assertTrue(is_prime(7))

    def test_not_prime(self):
        self.assertFalse(is_prime(9))

    def test_two_is_prime(self):
        self.assertTrue(is_prime(2))

    def test_one_is_not_prime(self):
        self.assertFalse(is_prime(1))

    def test_zero_is_not_prime(self):
        self.assertFalse(is_prime(0))

    def test_negative_is_not_prime(self):
        self.assertFalse(is_prime(-7))

    def test_large_prime(self):
        self.assertTrue(is_prime(97))

    def test_float_raises_type_error(self):
        with self.assertRaises(TypeError):
            is_prime(2.5)


class TestFibonacci(unittest.TestCase):

    def test_zero(self):
        self.assertEqual(fibonacci(0), 0)

    def test_one(self):
        self.assertEqual(fibonacci(1), 1)

    def test_fifth_number(self):
        self.assertEqual(fibonacci(5), 5)

    def test_tenth_number(self):
        self.assertEqual(fibonacci(10), 55)

    def test_negative_raises_value_error(self):
        with self.assertRaises(ValueError):
            fibonacci(-1)

    def test_float_raises_type_error(self):
        with self.assertRaises(TypeError):
            fibonacci(3.5)


class TestClamp(unittest.TestCase):

    def test_value_within_range(self):
        self.assertEqual(clamp(5, 1, 10), 5)

    def test_value_below_min(self):
        self.assertEqual(clamp(-5, 0, 10), 0)

    def test_value_above_max(self):
        self.assertEqual(clamp(20, 0, 10), 10)

    def test_value_equals_min(self):
        self.assertEqual(clamp(0, 0, 10), 0)

    def test_value_equals_max(self):
        self.assertEqual(clamp(10, 0, 10), 10)

    def test_invalid_range_raises_error(self):
        with self.assertRaises(ValueError):
            clamp(5, 10, 0)


class TestIsEven(unittest.TestCase):

    def test_even_number(self):
        self.assertTrue(is_even(4))

    def test_odd_number(self):
        self.assertFalse(is_even(3))

    def test_zero_is_even(self):
        self.assertTrue(is_even(0))

    def test_negative_even(self):
        self.assertTrue(is_even(-4))

    def test_negative_odd(self):
        self.assertFalse(is_even(-3))

    def test_float_raises_type_error(self):
        with self.assertRaises(TypeError):
            is_even(2.0)


class TestPower(unittest.TestCase):

    def test_positive_exponent(self):
        self.assertEqual(power(2, 3), 8)

    def test_zero_exponent(self):
        self.assertEqual(power(5, 0), 1)

    def test_negative_exponent(self):
        self.assertAlmostEqual(power(2, -1), 0.5)

    def test_base_zero(self):
        self.assertEqual(power(0, 5), 0)

    def test_float_exponent_raises_type_error(self):
        with self.assertRaises(TypeError):
            power(2, 1.5)


if __name__ == "__main__":
    unittest.main()