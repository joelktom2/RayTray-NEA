import re
def validlight(value):
    if re.fullmatch(r'-?\d+,-?\d+,-?\d+', value):
        return True
    return False


print(validlight('a,b,c')) # True