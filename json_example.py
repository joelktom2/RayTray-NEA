from object_table import get_object_data
import json

from objects import Sphere, Capsule
from Maths import Vector
from image import colour
capsule1 = Capsule(Vector(0,0,5),"y",6,1,colour(1,0,0),[0.5,0.5,0.0,0.0])
sphere = Sphere(Vector(0, 0, 5), 1.5, colour(0, 0, 1), [0.6, 0.2, 0.2, 0.4])
object_data = get_object_data(capsule1)
print(object_data)
# Convert object data to JSON
json_data = json.dumps(object_data, indent=4)
print(json_data)