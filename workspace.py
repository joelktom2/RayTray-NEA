import json
from Maths import Vector
from objects import Sphere
from image import colour

from object_table import save_object, load_objects, get_object_data

s1 = Sphere(Vector(0,0,2), 0.5, colour(0,1,0),[0.5,0.5,0.0,0.0],)

obj = s1

object_data = get_object_data(obj)



object_json = json.dumps(object_data)

print(object_json)