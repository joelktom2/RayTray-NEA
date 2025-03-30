from object_table import get_object_data
import json

from objects import Sphere
from Maths import Vector
from image import colour

sphere = Sphere(Vector(0, 0, 5), 1.5, colour(0, 0, 1), [0.6, 0.2, 0.2, 0.4])
object_data = get_object_data(sphere)
print(object_data)
# Convert object data to JSON
json_data = json.dumps(object_data, indent=4)
print(json_data)