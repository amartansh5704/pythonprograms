import unittest
from validator import UserValidator


class TestValidateUsername(unittest.TestCase):

    def setUp(self):
        self.validator = UserValidator()

    def test_valid_username(self):
        result, msg = self.validator.validate_username("john123")
        self.assertTrue(result)

    def test_too_short(self):
        result, msg = self.validator.validate_username("ab")
        self.assertFalse(result)

    def test_too_long(self):
        result, msg = self.validator.validate_username("a" * 21)
        self.assertFalse(result)

    def test_exactly_minimum_length(self):
        result, _ = self.validator.validate_username("abc")
        self.assertTrue(result)

    def test_exactly_maximum_length(self):
        result, _ = self.validator.validate_username("a" * 20)
        self.assertTrue(result)

    def test_special_characters(self):
        result, msg = self.validator.validate_username("john_doe")
        self.assertFalse(result)

    def test_spaces_not_allowed(self):
        result, _ = self.validator.validate_username("john doe")
        self.assertFalse(result)

    def test_non_string_raises_type_error(self):
        with self.assertRaises(TypeError):
            self.validator.validate_username(123)


class TestValidateEmail(unittest.TestCase):

    def setUp(self):
        self.validator = UserValidator()

    def test_valid_email(self):
        result, _ = self.validator.validate_email("user@example.com")
        self.assertTrue(result)

    def test_missing_at_symbol(self):
        result, _ = self.validator.validate_email("userexample.com")
        self.assertFalse(result)

    def test_missing_domain(self):
        result, _ = self.validator.validate_email("user@.com")
        self.assertFalse(result)

    def test_missing_extension(self):
        result, _ = self.validator.validate_email("user@example")
        self.assertFalse(result)

    def test_empty_string(self):
        result, _ = self.validator.validate_email("")
        self.assertFalse(result)

    def test_valid_email_with_dots(self):
        result, _ = self.validator.validate_email("first.last@example.com")
        self.assertTrue(result)

    def test_non_string_raises_type_error(self):
        with self.assertRaises(TypeError):
            self.validator.validate_email(123)


class TestValidatePassword(unittest.TestCase):

    def setUp(self):
        self.validator = UserValidator()

    def test_valid_password(self):
        result, _ = self.validator.validate_password("Secure1Password")
        self.assertTrue(result)

    def test_too_short(self):
        result, _ = self.validator.validate_password("Sh0rt")
        self.assertFalse(result)

    def test_no_uppercase(self):
        result, msg = self.validator.validate_password("secure1password")
        self.assertFalse(result)
        self.assertIn("uppercase", msg)

    def test_no_digit(self):
        result, msg = self.validator.validate_password("SecurePassword")
        self.assertFalse(result)
        self.assertIn("digit", msg)

    def test_exactly_8_characters_valid(self):
        result, _ = self.validator.validate_password("Secure1!")
        self.assertTrue(result)

    def test_empty_string(self):
        result, _ = self.validator.validate_password("")
        self.assertFalse(result)

    def test_non_string_raises_type_error(self):
        with self.assertRaises(TypeError):
            self.validator.validate_password(12345678)


class TestValidateAge(unittest.TestCase):

    def setUp(self):
        self.validator = UserValidator()

    def test_valid_age(self):
        result, _ = self.validator.validate_age(25)
        self.assertTrue(result)

    def test_minimum_valid_age(self):
        result, _ = self.validator.validate_age(13)
        self.assertTrue(result)

    def test_maximum_valid_age(self):
        result, _ = self.validator.validate_age(120)
        self.assertTrue(result)

    def test_age_too_young(self):
        result, msg = self.validator.validate_age(12)
        self.assertFalse(result)

    def test_age_too_old(self):
        result, msg = self.validator.validate_age(121)
        self.assertFalse(result)

    def test_zero_age(self):
        result, _ = self.validator.validate_age(0)
        self.assertFalse(result)

    def test_negative_age(self):
        result, _ = self.validator.validate_age(-1)
        self.assertFalse(result)

    def test_float_raises_type_error(self):
        with self.assertRaises(TypeError):
            self.validator.validate_age(25.5)


if __name__ == "__main__":
    unittest.main()