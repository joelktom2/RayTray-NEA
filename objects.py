import math
from material import material

class camera():
    def __init__(self,position):
        self.position = position

class Sphere():
    def __init__(self, center, radius,colour=(0,0,0),mat = [0.5,0.0,0.0]):
        self.center = center
        self.radius = radius
        self.colour = colour
        self.material = material(colour)
        self.material.shininess = mat[0]
        self.material.reflectivity = mat[1]
        self.material.transparency = mat[2]


    def __str__(self):
        return f"Center: {self.center}, Radius: {self.radius}, Colour: {self.colour}"
    
    def normal(self, point):
        return (point - self.center).norm()
    
    
    def intersects(self, ray):
        L = ray.origin - self.center
        a = ray.direction.dp(ray.direction)
        b = 2*((L).dp(ray.direction))
        c = (L).mag()**2 - self.radius**2
        if b**2 - (4*a*c) < 0:
            return None
        t1 =  (-(b) + (math.sqrt(b**2 - (4*a*c))) ) /(2*a)
        t2 =  ( -(b) - (math.sqrt(b**2 - (4*a*c))) ) /(2*a)
        if t1 < t2 and t1>= 0:
            return ray.point(t1)
        else:
            return ray.point(t2)
           

class Plane():
    
    def __init__(self, point, normal):
        self.point = point
        self.normal = normal

    def __str__(self):
        return "{}x + {}y + {}z = {}".format(self.normal.x, self.normal.y, self.normal.z, self.point.dp(self.normal))

    def intersects(self, ray):
        t = (self.point - ray.origin).dp(self.normal) / ray.direction.dp(self.normal)
        if t < 0:
            return None
        return t
    


