import math
from material import material
from image import colour

class camera():
    def __init__(self,position):
        self.position = position   # (x,y,z) coordinates of the camera

class Sphere():
    def __init__(self, center, radius,colour=(0,0,0),mat = [0.5,0.0,0.0]):
        self.center = center       # (x,y,z) coordinates of the center of the sphere
        self.radius = radius       # radius of the sphere integer 
        self.colour = colour        # colour of the sphere (r,g,b)
        self.material = material(colour)  # material properties of the sphere
        self.material.shininess = mat[0]  # shininess of the sphere
        self.material.reflectivity = mat[1]  # reflectivity of the sphere
        self.material.transparency = mat[2]  # transparency of the sphere


    def __str__(self):
        return f"Center: {self.center}, Radius: {self.radius}, Colour: {self.colour}"
    
    def get_normal(self, point):   #nomral to get_normal
        return (point - self.center).norm()   # returns the normal vector at a point on the sphere
    
    
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
            return ray.point(t2)      # returns the point of intersections of the ray with the sphere
           

class Plane():
    
    def __init__(self, point, normal,colour=colour(0,0,1),mat = [0.5,0.0,0.0]):
        self.point = point
        self.normal = normal
        self.colour = colour        # colour of the sphere (r,g,b)
        self.material = material(colour)  # material properties of the sphere
        self.material.shininess = mat[0]  # shininess of the sphere
        self.material.reflectivity = mat[1]  # reflectivity of the sphere
        self.material.transparency = mat[2]

    def __str__(self):
        return "{}x + {}y + {}z = {}".format(self.normal.x, self.normal.y, self.normal.z, self.point.dp(self.normal))

    def intersects(self, ray):
        t = (self.point - ray.origin).dp(self.normal) / ray.direction.dp(self.normal)
        
        if t < 0:
            return None
        return ray.point(t)   # returns the point of intersection of the ray with the plane
    
    def get_normal(self, point):
        return self.normal.norm()

