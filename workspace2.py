from Maths import Vector

def string_coords_to_Vector(value):
    position_parts = value.split(",")
    x, y, z = map(float, position_parts)
    return Vector(x, y, z)

print(string_coords_to_Vector("1.4,2,3"))  # Output: Vector(1, 2, 3)