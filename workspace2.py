from Maths import Vector, Ray
from objects import Cone
import math

ray = Ray(Vector(1, -5, 0), Vector(0, 1, 0))
cone = Cone(Vector(0, 0, 0), Vector(0, 1, 0), math.radians(45))

intersection = cone.intersects(ray)

print(intersection)