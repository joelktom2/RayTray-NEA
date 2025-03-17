import re

def password_sanitate(value):

    if len(value) < 8:
        return False
    elif not(re.search(r"[A-Z]",value)):
        return False 
    elif not(re.search(r"[\d]",value)):
        return False
    elif not(re.search(r"[!@\$%\^&\*\+#]",value)):
        return False
    return True     


while True:
    password = input("Enter a password: ")
    if password_sanitate(password):
        print("Password is valid")
        break
    else:
        print("Password is invalid")
        continue