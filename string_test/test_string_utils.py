import unittest
from string_utils import (
    reverse_string,
    is_palindrome,
    count_vowels,
    capitalize_words,
    remove_whitespace,
    count_words
)


class TestReverseString(unittest.TestCase):

    def test_regular_string(self):
        self.assertEqual(reverse_string("hello"), "olleh")

    def test_single_character(self):
        self.assertEqual(reverse_string("a"), "a")

    def test_empty_string(self):
        self.assertEqual(reverse_string(""), "")

    def test_string_with_spaces(self):
        self.assertEqual(reverse_string("hello world"), "dlrow olleh")

    def test_numbers_as_string(self):
        self.assertEqual(reverse_string("12345"), "54321")

    def test_raises_type_error(self):
        with self.assertRaises(TypeError):
            reverse_string(123)


class TestIsPalindrome(unittest.TestCase):

    def test_simple_palindrome(self):
        self.assertTrue(is_palindrome("racecar"))

    def test_not_palindrome(self):
        self.assertFalse(is_palindrome("hello"))

    def test_palindrome_with_spaces(self):
        self.assertTrue(is_palindrome("race car"))

    def test_mixed_case_palindrome(self):
        self.assertTrue(is_palindrome("RaceCar"))

    def test_empty_string(self):
        self.assertTrue(is_palindrome(""))

    def test_single_character(self):
        self.assertTrue(is_palindrome("a"))

    def test_raises_type_error(self):
        with self.assertRaises(TypeError):
            is_palindrome(123)


class TestCountVowels(unittest.TestCase):

    def test_all_vowels(self):
        self.assertEqual(count_vowels("aeiou"), 5)

    def test_no_vowels(self):
        self.assertEqual(count_vowels("gym"), 0)

    def test_mixed_string(self):
        self.assertEqual(count_vowels("hello"), 2)

    def test_empty_string(self):
        self.assertEqual(count_vowels(""), 0)

    def test_uppercase_vowels(self):
        self.assertEqual(count_vowels("AEIOU"), 5)

    def test_raises_type_error(self):
        with self.assertRaises(TypeError):
            count_vowels(999)


class TestCapitalizeWords(unittest.TestCase):

    def test_lowercase_words(self):
        self.assertEqual(capitalize_words("hello world"), "Hello World")

    def test_already_capitalized(self):
        self.assertEqual(capitalize_words("Hello World"), "Hello World")

    def test_single_word(self):
        self.assertEqual(capitalize_words("python"), "Python")

    def test_empty_string(self):
        self.assertEqual(capitalize_words(""), "")

    def test_raises_type_error(self):
        with self.assertRaises(TypeError):
            capitalize_words(42)


class TestRemoveWhitespace(unittest.TestCase):

    def test_leading_spaces(self):
        self.assertEqual(remove_whitespace("  hello"), "hello")

    def test_trailing_spaces(self):
        self.assertEqual(remove_whitespace("hello  "), "hello")

    def test_both_sides(self):
        self.assertEqual(remove_whitespace("  hello  "), "hello")

    def test_no_spaces(self):
        self.assertEqual(remove_whitespace("hello"), "hello")

    def test_empty_string(self):
        self.assertEqual(remove_whitespace(""), "")

    def test_raises_type_error(self):
        with self.assertRaises(TypeError):
            remove_whitespace(100)


class TestCountWords(unittest.TestCase):

    def test_multiple_words(self):
        self.assertEqual(count_words("hello world"), 2)

    def test_single_word(self):
        self.assertEqual(count_words("hello"), 1)

    def test_empty_string(self):
        self.assertEqual(count_words(""), 0)

    def test_only_spaces(self):
        self.assertEqual(count_words("   "), 0)

    def test_raises_type_error(self):
        with self.assertRaises(TypeError):
            count_words(55)


if __name__ == "__main__":
    unittest.main()