import math
from material import material
from image import colour


class camera():
    def __init__(self,position):
        self.position = position   # (x,y,z) coordinates of the camera

class Sphere():
    def __init__(self, center, radius,colour=colour(0,0,0),mat = [0.5,0.5,0.0,0.0],texture = None):
        self.center = center       # (x,y,z) coordinates of the center of the sphere
        self.radius = radius       # radius of the sphere integer 
        self.colour = colour        #base colour of the sphere (r,g,b)
        self.material = material(colour,mat[0],mat[1],mat[2],mat[3],texture)  # material properties of the sphere


    def __str__(self):
        return f"Center: {self.center}, Radius: {self.radius}, Colour: {self.colour}"
    
    def get_normal(self, point):   #nomral to get_normal
        return (point - self.center).norm()   # returns the normal vector at a point on the sphere
    
    
    def intersects(self, ray):
        
        l = ray.origin - self.center
        a = 1
        b = 2*((l).dp(ray.direction))
        c = (l).mag()**2 - self.radius**2
        discrminant = b**2 - (4*a*c)
    
        if discrminant < -1e-6:
            return None
            
        elif discrminant == 0 or abs(discrminant) < 1e-6:
            t =  (-(b)) /(2*a)
            if t>= 0:
                return ray.point(t)
            else:
                return None
            
        t1 =  (-(b) + (math.sqrt(b**2 - (4*a*c))) ) /(2*a)
        t2 =  ( -(b) - (math.sqrt(b**2 - (4*a*c))) ) /(2*a)
    
        if abs((ray.origin - self.center).mag() - self.radius) < 1e-6:
            return ray.point(max(t1, t2))
            
        if t1 >= 0 and t2>= 0:
            return ray.point(min(t1, t2))                
        
        elif t1 >= 0:
            return ray.point(t1)  
        
        elif t2 >= 0:
            return ray.point(t2)  
        else:
            return None 
        
           

class Plane():
    
    def __init__(self, point, normal,colour=colour(0,0,1),mat = [0.5,0.0,0.0]):
        self.point = point
        self.normal = normal
        self.colour = colour        # colour of the sphere (r,g,b)
        self.material = material(colour,mat[0],mat[1],mat[2])  # material properties of the sphere
        

    def __str__(self):
        return "{}x + {}y + {}z = {}".format(self.normal.x, self.normal.y, self.normal.z, self.point.dp(self.normal))

    def intersects(self, ray):
        t = (self.point - ray.origin).dp(self.normal) / ray.direction.dp(self.normal)
        
        if t < 0:
            return None
        return ray.point(t)   # returns the point of intersection of the ray with the plane
    
    def get_normal(self, point):
        return self.normal.norm()


