import re

def is_valid_password(password):
    
    allowed_special_characters = r"~`!@#$%^&*()+=_\-{}[\]\\|:;”’?/<>,."
    pattern = rf"[A-Za-z0-9{re.escape(allowed_special_characters)}]+"
    if re.fullmatch(pattern, password):
        return True
    return False

# Example Usage
print(is_valid_password("Password123"))  # True
print(is_valid_password("Pass@word123"))  # True
print(is_valid_password("Pass#word!123"))  # True
print(is_valid_password("Password 123"))  # False (contains space)
print(is_valid_password("Password<123>"))  # True
