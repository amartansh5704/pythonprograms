import string

def check_length(password):
    return len(password) >= 8

def check_uppercase(password):
    for char in password:
        if char.isupper():
            return True
    return False
def check_lowercase(password):
    for char in password:
        if char.islower():
            return True
    return False
def check_digit(password):
    for char in password:
        if char.isdigit():
            return True
    return False
def check_special_char(password):
    special_chars = string.punctuation
    for char in password:
        if char in special_chars:
            return True
    return False
def get_password_strength(password):
    strength = 0
    if check_length(password):
        strength += 1
    else:
        print("Password must be at least 8 characters long.")
    if check_uppercase(password):
        strength += 1
    else:
        print("Password must contain at least one uppercase letter.")
    if check_lowercase(password):
        strength += 1
    else:
        print("Password must contain at least one lowercase letter.")
    if check_digit(password):
        strength += 1
    else:
        print("Password must contain at least one digit.")
    if check_special_char(password):
        strength += 1
    else:
        print("Password must contain at least one special character.")
    return strength

def display_strength(strength):
    if strength == 5:
        print("Password Strength: Very Strong")
    elif strength == 4:
        print("Password Strength: Strong")
    elif strength == 3:
        print("Password Strength: Medium")
    elif strength == 2:
        print("Password Strength: Weak")
    else:
        print("Password Strength: Very Weak")

print("=" * 40)
print("    🔐 PASSWORD STRENGTH CHECKER")
print("=" * 40)

while True:
    password = input("Enter a password to check its strength")
    strength = get_password_strength(password)
    display_strength(strength)
