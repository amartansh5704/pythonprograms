import re


class UserValidator:

    def validate_username(self, username):
        if not isinstance(username, str):
            raise TypeError("Username must be a string")
        if len(username) < 3:
            return False, "Username must be at least 3 characters"
        if len(username) > 20:
            return False, "Username must be at most 20 characters"
        if not username.isalnum():
            return False, "Username must contain only letters and numbers"
        return True, "Valid"

    def validate_email(self, email):
        if not isinstance(email, str):
            raise TypeError("Email must be a string")
        pattern = r"^[\w\.-]+@[\w\.-]+\.\w{2,4}$"
        if re.match(pattern, email):
            return True, "Valid"
        return False, "Invalid email format"

    def validate_password(self, password):
        if not isinstance(password, str):
            raise TypeError("Password must be a string")
        if len(password) < 8:
            return False, "Password must be at least 8 characters"
        if not any(char.isupper() for char in password):
            return False, "Password must contain at least one uppercase letter"
        if not any(char.isdigit() for char in password):
            return False, "Password must contain at least one digit"
        return True, "Valid"

    def validate_age(self, age):
        if not isinstance(age, int):
            raise TypeError("Age must be an integer")
        if age < 13:
            return False, "Must be at least 13 years old"
        if age > 120:
            return False, "Age is not realistic"
        return True, "Valid"