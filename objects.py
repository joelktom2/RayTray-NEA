import math
from material import material
from image import colour




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
        discriminant = b**2 - (4*a*c)
    
        if discriminant < -1e-6:
            return None
            
        elif discriminant == 0 or abs(discriminant) < 1e-6:
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
        
           

class Cone():
    def __init__(self, tip,axis,angle,height=None,colour=colour(0,0,0),mat = [0.5,0.5,0.0,0.0],texture = None):
        self.tip = tip       # (x,y,z) coordinates of the tip of the cone
        self.axis = axis.norm()     # (x,y,z) coordinates of the axis of the cone
        self.angle = angle      # angle between axis and the side of the cone
        self.height = height    # height of the cone
        self.colour = colour        #base colour of the sphere (r,g,b)
        self.material = material(colour,mat[0],mat[1],mat[2],mat[3],texture)  # material properties of the sphere


    def __str__(self):
        return f"Tip: {self.tip}, Axis: {self.axis}, Colour: {self.colour}"
    
    def get_normal(self, point):
        s = point - self.tip  # Vector from tip to point
        d = self.axis * abs(s.dp(self.axis)) # Project s onto the axis
        a = s - d  # Vector from the axis to the point
        n = a - self.axis * (math.tan(self.angle) * a.mag())  # Normal to the cone at the point
        return n.norm()  # Normalize the normal
    
   
    def intersects(self, ray):
        D = ray.direction.norm()  # Ensure normalized ray direction
        V = self.axis.norm()      # Normalized cone axis
        OC = ray.origin - self.tip  # Vector from cone tip to ray origin
        cos_theta = math.cos(self.angle)    # Cosine of the cone half-angle
        cos2_theta = cos_theta ** 2
        d_dot_v = D.dp(V)
        oc_dot_v = OC.dp(V)
        
        #quadratic coefficients for intersection formula
        a = d_dot_v**2 - cos2_theta
        b = 2 * ((d_dot_v * oc_dot_v) - D.dp(OC) * cos2_theta)
        c = oc_dot_v**2 - cos2_theta * OC.dp(OC)

        if a == 0 or abs(a) < 1e-6:
            # Ray is parallel to the cone axis
            return None
        
        discriminant = b**2 - 4*a*c

        # No intersection if discriminant is negative
        if discriminant < -1e-6:
            return None
        
        if discriminant == 0 or abs(discriminant) < 1e-6:
            t =  (-(b)) /(2*a)
            if t>= 0:
                return ray.point(t)
            else:
                return None

        sqrt_disc = math.sqrt(discriminant)
        t1 = (-b + sqrt_disc) / (2 * a)
        t2 = (-b - sqrt_disc) / (2 * a)

        def is_valid(t): #ensure the intersection is within the height of the cone and are in front of camera
            if t < 0:
                return False
            point = ray.point(t)
            h = (point - self.tip).dp(V)
            if self.height:
                h_max = self.height 
                return h >= 0 and h <= h_max
            return h >= 0
           
        def intersects_cap(): # Check for intersection with the cone's base
            
            radius_at_h_max = self.height * math.tan(self.angle)
            t_cap = ((self.tip + V * self.height - ray.origin).dp(V)) / d_dot_v
            if t_cap < 0:
                return None
            point_cap = ray.point(t_cap)
            # Check if the point is within the radius of the base
            if (point_cap - (self.tip + V * self.height)).mag() <= radius_at_h_max:
                return t_cap
            return None
        
        intersections = [t for t in (t1, t2) if is_valid(t)]
        if self.height:
            t3 = intersects_cap()
            if t3:
                intersections.append(t3)

        return ray.point(min(intersections)) if intersections else None


       

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





