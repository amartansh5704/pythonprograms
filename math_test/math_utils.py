def factorial(n):
    if not isinstance(n, int):
        raise TypeError("Input must be an integer")
    if n < 0:
        raise ValueError("Input must be a non-negative integer")
    if n == 0 or n == 1:
        return 1
    return n * factorial(n - 1)


def is_prime(n):
    if not isinstance(n, int):
        raise TypeError("Input must be an integer")
    if n < 2:
        return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True


def fibonacci(n):
    if not isinstance(n, int):
        raise TypeError("Input must be an integer")
    if n < 0:
        raise ValueError("Input must be a non-negative integer")
    if n == 0:
        return 0
    if n == 1:
        return 1
    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    return b


def clamp(value, min_val, max_val):
    if min_val > max_val:
        raise ValueError("min_val cannot be greater than max_val")
    return max(min_val, min(value, max_val))


def is_even(n):
    if not isinstance(n, int):
        raise TypeError("Input must be an integer")
    return n % 2 == 0


def power(base, exponent):
    if not isinstance(exponent, int):
        raise TypeError("Exponent must be an integer")
    return base ** exponent