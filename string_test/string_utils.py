def reverse_string(s):
    if not isinstance(s, str):
        raise TypeError("Input must be a string")
    return s[::-1]


def is_palindrome(s):
    if not isinstance(s, str):
        raise TypeError("Input must be a string")
    cleaned = s.lower().replace(" ", "")
    return cleaned == cleaned[::-1]


def count_vowels(s):
    if not isinstance(s, str):
        raise TypeError("Input must be a string")
    return sum(1 for char in s.lower() if char in "aeiou")


def capitalize_words(s):
    if not isinstance(s, str):
        raise TypeError("Input must be a string")
    return " ".join(word.capitalize() for word in s.split())


def remove_whitespace(s):
    if not isinstance(s, str):
        raise TypeError("Input must be a string")
    return s.strip()


def count_words(s):
    if not isinstance(s, str):
        raise TypeError("Input must be a string")
    if s.strip() == "":
        return 0
    return len(s.split())