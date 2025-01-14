from objects import Plane
from Maths import Ray,Vector
from image import colour

p1 = Plane(Vector(0,5,0),Vector(0,1,0))
print(p1)
r1 = Ray(Vector(0,0,-1),Vector(0,20,10))
print(p1.intersects(r1))

c1 = colour(1,0,0)

print(c1*2.2354593073396356e-05)