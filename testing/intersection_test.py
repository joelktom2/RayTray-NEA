import math
class Sphere():
    def __init__(self, center, radius):
        self.center = center
        self.radius = radius

    def __str__(self):
        return f"Center: {self.center}, Radius: {self.radius}"
    
    def intersection(self, ray):
        L = ray.origin - self.center
        a = ray.direction.dp(ray.direction)
        b = 2*((L).dp(ray.direction))
        c = (L).mag()**2 - self.radius**2
        if b**2 - (4*a*c) < 0:
            return None
        t1 =  (-(b) + (math.sqrt(b**2 - (4*a*c))) ) /(2*a)
        t2 =  ( -(b) - (math.sqrt(b**2 - (4*a*c))) ) /(2*a)
        return t1,t2

class Ray():
    def __init__(self, origin, direction):
        self.origin = origin
        self.direction = direction

    def point_at_parameter(self, t):
        return (self.origin) + (t * self.direction)

class Vector():
    def __init__(self, x, y , z):
        self.x = x
        self.y = y
        self.z = z

    def __str__(self):
        return f"[{self.x},{self.y},{self.z}]"
    
    def values(self):
        list = [self.x,self.y,self.z]
        print(list)    

    def __add__(self,v2):
        return Vector((self.x+v2.x),(self.y+v2.y),(self.z+v2.z))
        
    def __sub__(self,v2):
        return Vector((self.x-v2.x),(self.y-v2.y),(self.z-v2.z))
         
    def __mul__(self,scale):
        return Vector((self.x)*scale,(self.y)*scale,(self.z)*scale)
        
    def __truediv__(self,scale):
        return Vector((self.x)/scale,(self.y)/scale,(self.z)/scale)

    def dp(self,v2):
        return self.x*v2.x + self.y*v2.y + self.z*v2.z
 
    def cp(self,v2):
        return Vector((self.y*v2.z-self.z*v2.y),(self.z*v2.x-self.x*v2.z),(self.x*v2.y-self.y*v2.x))

    def mag(self):
        return math.sqrt(((self.x)**2+(self.y)**2+(self.z)**2))

    def norm(self):
        m = self.mag()
        return Vector((self.x)/m,(self.y)/m,(self.z)/m)
    
    def angle(self,v2):
        return math.acos(self.dp(v2)/(self.mag()*v2.mag()))

    def proj(self,v2):
        return (self.dp(v2)/v2.mag())

ray1 = Ray(Vector(0,0,-5),Vector(0,0,1))
sphere1 = Sphere(Vector(0,0,0),1)
t1,t2 = sphere1.intersection(ray1)
print(t1)
print(t2)