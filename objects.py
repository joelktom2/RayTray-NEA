import math
from material import material
from image import colour
from Maths import Vector,Matrix



class Shape:  #parent class for all the different objects
    def __init__(self,colour=colour(0,0,0), mat=[0.5,0.5,0.0,0.0], texture=None):
        self.colour = colour      # Base colour of the object            
        self.material = material(colour, mat[0], mat[1], mat[2], mat[3], texture) #material properties of the object
    
    def get_normal(self, point):
        raise NotImplementedError("Subclasses must implement get_normal")   #ensure the subclasses implement this method
    
    def intersects(self, ray):
        raise NotImplementedError("Subclasses must implement intersects") #ensure the subclasses implement this method
    
    def __str__(self):
        return f"Position: {self.position}, Colour: {self.colour}"


class Sphere(Shape):
    def __init__(self, center, radius,colour=colour(0,0,0),mat = [0.5,0.5,0.0,0.0],texture = None):
        super().__init__(colour, mat, texture)
        self.center = center       # (x,y,z) coordinates of the center of the sphere
        self.radius = radius       # radius of the sphere integer 

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
        
class Floor(Sphere):
    def __init__(self,colour=colour(0,0,0),mat = [0.5,0.5,0.0,0.0],texture = None):
        super().__init__(Vector(0,10000.5,1), 10000, colour, mat, texture)
    

class Cone(Shape):
    def __init__(self,tip,axis,angle,height=None,colour=colour(0,0,0),mat = [0.5,0.5,0.0,0.0],texture = None):
        super().__init__(colour, mat, texture)
        self.tip = tip       # (x,y,z) coordinates of the tip of the cone
        self.axis = axis.norm()     # (x,y,z) coordinates of the axis of the cone
        self.angle = angle      # angle between axis and the side of the cone
        self.height = height    # height of the cone

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
            h = abs((point - self.tip).dp(V))
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


class Cylinder(Shape):  
    def __init__(self,center,allingment,height,radius,colour=colour(0,0,0),mat = [0.5,0.5,0.0,0.0],texture = None):
        super().__init__(colour, mat, texture)
        self.center = center       # (x,y,z) coordinates of the center of the Ellipsoid
        if allingment == 'x':
            self.axis = Vector(1,0,0)
            self.abc = Vector(100,radius,radius)
        elif allingment == 'y':
            self.axis = Vector(0,1,0)
            self.abc = Vector(radius,100,radius)
        elif allingment == 'z':
            self.axis = Vector(0,0,1)
            self.abc = Vector(radius,radius,100)
        self.height = height
        self.radius = radius   #  a b and c values of the ellipsoid
        

    def __str__(self):
        return f"Center: {self.center}, Radius: {self.abc}, Colour: {self.colour} texture : {self.material.texture}"

    def get_normal(self, point):
        return Vector((point.x - self.center.x) / self.abc.x**2,
                      (point.y - self.center.y) / self.abc.y**2,
                      (point.z - self.center.z) / self.abc.z**2).norm()
    
    def intersects(self, ray):
        l = ray.origin - self.center
        a = (ray.direction.x / self.abc.x)**2 + (ray.direction.y / self.abc.y)**2 + (ray.direction.z / self.abc.z)**2
        b = 2 * ((l.x * ray.direction.x / self.abc.x**2) + (l.y * ray.direction.y / self.abc.y**2) + (l.z * ray.direction.z / self.abc.z**2))
        c = (l.x / self.abc.x)**2 + (l.y / self.abc.y)**2 + (l.z / self.abc.z)**2 - 1
        discriminant = b**2 - (4 * a * c)
        
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


        def intersects_cap():
            if abs(ray.direction.dp(self.axis)) < 1e-6:
                return None
            top_cap = self.center + self.axis * (self.height / 2)
            bottom_cap = self.center + self.axis*(self.height / 2)
            top = ((top_cap - ray.origin).dp(self.axis)) / ray.direction.dp(self.axis)
            bottom = ((bottom_cap - ray.origin).dp(self.axis)) / ray.direction.dp(self.axis)
            if top and bottom:
                t_cap = min(top, bottom)
                point_cap = ray.point(t_cap)
                if ((point_cap - top_cap).mag())**2 <= self.radius ** 2:
                    return t_cap
                
            elif top:
                t_cap = top
                point_cap = ray.point(t_cap)
                if ((point_cap - top_cap).mag())**2 <= self.radius ** 2:
                    return t_cap

            elif bottom:
                t_cap = bottom
                point_cap = ray.point(t_cap)
                if (point_cap - bottom_cap).mag2() <= self.radius ** 2:
                    return t_cap
            return None
        
        
        def is_valid(t):
            # Check if the point is within the height of the cylinder
            if t < 0:
                return False
            point = ray.point(t)
            # Project the vector (point - center) onto the axis to get height
            height_projection = (point - self.center).dp(self.axis)
            return abs(height_projection) <= (self.height/2) 
        
        intersections = [t for t in (t1, t2) if is_valid(t)]
        t3 = intersects_cap()
        if t3:
            intersections.append(t3)
        return ray.point(min(intersections)) if intersections else None


class Ellipsoid(Shape):
    def __init__(self,center,abc=Vector(1,1,1),colour=colour(0,0,0),mat = [0.5,0.5,0.0,0.0],texture = None):
        super().__init__(colour, mat, texture)
        self.center = center       # (x,y,z) coordinates of the center of the Ellipsoid
        self.abc =  abc      #  a b and c values of the ellipsoid taken as a vector for simplicity



    def __str__(self):
        return f"Center: {self.center}, Radius: {self.abc}, Colour: {self.colour} texture : {self.material.texture}"

    def get_normal(self, point):
        return Vector((point.x - self.center.x) / self.abc.x**2,
                      (point.y - self.center.y) / self.abc.y**2,
                      (point.z - self.center.z) / self.abc.z**2).norm()
    
    def intersects(self, ray):
        l = ray.origin - self.center
        a = (ray.direction.x / self.abc.x)**2 + (ray.direction.y / self.abc.y)**2 + (ray.direction.z / self.abc.z)**2
        b = 2 * ((l.x * ray.direction.x / self.abc.x**2) + (l.y * ray.direction.y / self.abc.y**2) + (l.z * ray.direction.z / self.abc.z**2))
        c = (l.x / self.abc.x)**2 + (l.y / self.abc.y)**2 + (l.z / self.abc.z)**2 - 1
        discriminant = b**2 - (4 * a * c)
        
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
    
        if t1 >= 0 and t2>= 0:
            return ray.point(min(t1, t2))                
        
        elif t1 >= 0:
            return ray.point(t1)  
        
        elif t2 >= 0:
            return ray.point(t2)  
        else:
            return None


class Cube(Shape):
    def __init__(self, center, side_length, rotation=Vector(0, 0, 0), colour=colour(0, 0, 0), mat=[0.5, 0.5, 0.0, 0.0], texture=None):
        super().__init__(colour, mat, texture)
        self.center = center
        self.side_length = side_length


        # Build rotation matrix
        self.rotation = rotation
        self.rotation_matrix = Matrix.get_combined_rotation_matrix(rotation)
        self.inverse_rotation_matrix = self.rotation_matrix.inverse()

        # Local space AABB (unrotated)
        half = side_length / 2
        self.local_min = Vector(-half, -half, -half)
        self.local_max = Vector(half, half, half)

    def get_normal(self, point):
        # Transform point into local space
        local_point = Matrix.rotate_vector(point - self.center, self.inverse_rotation_matrix)

        # Determine face normal in local space
        epsilon = 1e-5
        if abs(local_point.x - self.local_max.x) < epsilon:
            normal = Vector(1, 0, 0)
        elif abs(local_point.x - self.local_min.x) < epsilon:
            normal = Vector(-1, 0, 0)
        elif abs(local_point.y - self.local_max.y) < epsilon:
            normal = Vector(0, 1, 0)
        elif abs(local_point.y - self.local_min.y) < epsilon:
            normal = Vector(0, -1, 0)
        elif abs(local_point.z - self.local_max.z) < epsilon:
            normal = Vector(0, 0, 1)
        elif abs(local_point.z - self.local_min.z) < epsilon:
            normal = Vector(0, 0, -1)
        else:
            normal = Vector(0, 0, 0)  # fallback

        # Rotate normal back to world space
        return Matrix.rotate_vector(normal, self.rotation_matrix).norm()

    def intersects(self, ray):
        # Step 1: Transform ray into cube's local space
        local_origin = Matrix.rotate_vector(ray.origin - self.center, self.inverse_rotation_matrix)
        local_direction = Matrix.rotate_vector(ray.direction, self.inverse_rotation_matrix)

        # Step 2: Perform standard AABB ray-box intersection in local space
        t_min = -float('inf')
        t_max = float('inf')
        for axis in ['x', 'y', 'z']:
            origin_val = getattr(local_origin, axis)
            direction_val = getattr(local_direction, axis)
            min_val = getattr(self.local_min, axis)
            max_val = getattr(self.local_max, axis)

            if abs(direction_val) < 1e-6:
                if origin_val < min_val or origin_val > max_val:
                    return None  # no intersection
            else:
                t1 = (min_val - origin_val) / direction_val
                t2 = (max_val - origin_val) / direction_val
                t1, t2 = min(t1, t2), max(t1, t2)
                t_min = max(t_min, t1)
                t_max = min(t_max, t2)
                if t_max < t_min:
                    return None

        if t_min < 0:
            return None  # intersection is behind the ray

        # Step 3: Convert hit point back to world space
        hit_local = local_origin + local_direction * t_min
        hit_world = Matrix.rotate_vector(hit_local, self.rotation_matrix) + self.center
        return hit_world


class Triangle(Shape):
    def __init__(self,v0,v1,v2,colour=colour(0,0,0),mat = [0.5,0.5,0.0,0.0],texture = None):
        super().__init__(colour, mat, texture)
        self.v0 = v0
        self.v1 = v1
        self.v2 = v2
    
    def intersects(self, ray):
        EPSILON = 1e-6
        v0 = self.v0
        v1 = self.v1
        v2 = self.v2
        
        edge1 = v1 - v0
        edge2 = v2 - v0
        h = ray.direction.cp(edge2)
        a = edge1.dp(h)
        
        if -EPSILON < a < EPSILON:
            return None  # Ray is parallel to the triangle
        
        f = 1.0 / a
        s = ray.origin - v0
        u = f * s.dp(h)
        
        if u < 0.0 or u > 1.0:
            return None
        
        q = s.cp(edge1)
        v = f * ray.direction.dp(q)
        
        if v < 0.0 or u + v > 1.0:
            return None
        
        t = f * edge2.dp(q)
        
        if t > EPSILON:
            # print(ray.point(t))
            return ray.point(t)  # intersection point
        else:
            return None  # intersection behind the origin
        
    def get_normal(self):
        edge1 = self.v1 - self.v0
        edge2 = self.v2 - self.v0
        return (edge1.cp(edge2)).norm()
    def contains(self, point):
        # Same as barycentric check, but built into the Triangle
        epsilon=1e-6
        v0 = self.v0
        v1 = self.v1
        v2 = self.v2
        u = v1 - v0
        v = v2 - v0
        w = point - v0

        uu = u.dp(u)
        uv = u.dp(v)
        vv = v.dp(v)
        wu = w.dp(u)
        wv = w.dp(v)

        denom = uv * uv - uu * vv
        if abs(denom) < epsilon:
            return False  # Degenerate triangle

        s = (uv * wv - vv * wu) / denom
        t = (uv * wu - uu * wv) / denom

        return (s >= -epsilon) and (t >= -epsilon) and (s + t <= 1 + epsilon)


def tetrahedron_vertices(center, side_length):
    # Height from base to apex
    h = math.sqrt(2/3) * side_length

    # Radius of base triangle from center
    r = side_length / math.sqrt(3)

    # z-offset to center tetrahedron at origin
    z_offset = -h / 4

    # Base triangle (equilateral, in xy-plane, centered below origin)
    v1 = Vector(r, 0, z_offset)
    v2 = Vector(-r/2,  (r * math.sqrt(3))/2, z_offset)
    v3 = Vector(-r/2, -(r * math.sqrt(3))/2, z_offset)

    # Apex above the base
    v4 = Vector(0, 0, h * 3/4)

    # Translate all points so that the centroid is at 'center'
    vertices = [v1, v2, v3, v4]
    centroid = sum(vertices, Vector(0, 0, 0)) * (1 / 4)
    offset = center - centroid
    vertices = [v + offset for v in vertices]
    return vertices[0],vertices[1],vertices[2],vertices[3]

class Tetrahedron(Shape):
    def __init__(self, center, radius,colour=colour(1,0,0),mat = [0.5,0.5,0.0,0.0],texture = None):
        super().__init__(colour, mat, texture)
        self.center = center       # (x,y,z) coordinates of the center of the sphere
        self.radius = radius       # radius of the sphere integer 
        a, b, c, d = tetrahedron_vertices(center,radius)
        self.faces = [
            Triangle(c,b,a, colour, mat, texture),
            Triangle(d,b,a, colour, mat, texture),
            Triangle(d,c,a, colour, mat, texture),
            Triangle(d,c,b, colour, mat, texture)
        ]

    def intersects(self, ray):
        intersections = [face.intersects(ray) for face in self.faces]
        intersections = [p for p in intersections if p is not None]
        if intersections:
            return min(intersections, key=lambda p: (p - ray.origin).mag())
        return None
    
    def get_normal(self,point):
        # You might want to find which face the point lies on and return that normal.
        for face in self.faces:
            if face.contains(point):  # You'd implement this in Triangle
                return face.get_normal()
        return None