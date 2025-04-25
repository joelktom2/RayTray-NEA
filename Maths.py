import math

class Vector():    
    def __init__(self, x, y , z):
        self.x = x
        self.y = y
        self.z = z

    def __str__(self):
        return f"[{self.x},{self.y},{self.z}]"
    
    def values(self):
        return [self.x,self.y,self.z]
        

    def __eq__(self, other):
        if isinstance(other, Vector):
            return self.x == other.x and self.y == other.y and self.z == other.z
        return False    

    def __add__(self,v2):
        return Vector((self.x+v2.x),(self.y+v2.y),(self.z+v2.z))
        
    def __sub__(self,v2):
        return Vector((self.x-v2.x),(self.y-v2.y),(self.z-v2.z))
         
    def __neg__(self):
        return Vector(-self.x, -self.y, -self.z)
    
    
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
        return self/self.mag()
        
    
    def angle(self,v2):
        return math.acos(self.dp(v2)/(self.mag()*v2.mag()))

    def proj(self,v2):
        return (self.dp(v2)/v2.mag())
    
    
    
class Matrix():
    def __init__(self,elements):

        self.row = len(elements)
        self.column = len(elements[0])
        self.elements = elements
    
    def __str__(self):
        return f"{self.elements}"
    

    def zero(rows, cols):
        return Matrix([[0 for _ in range(cols)] for _ in range(rows)])
    
    def __add__(self,m2):
        if self.row == m2.row and self.column == m2.column:
            m3 = Matrix.zero(self.row, self.column)
            for x in range(self.row):
                for y in range(self.column):
                    m3.elements[x][y] = self.elements[x][y] + m2.elements[x][y]
        
            return m3
        else:
            return None
        
    def __sub__(self,m2):
        
        if self.row == m2.row and self.column == m2.column:
            m3 = Matrix.zero(self.row, self.column)
            for x in range(self.row):
                for y in range(self.column):
                    m3.elements[x][y] = self.elements[x][y] - m2.elements[x][y]
        
            return m3
        else:
            return None
    
    
    def __mul__(self, other):
        # Matrix × Matrix
        if isinstance(other, Matrix):
            if self.column != other.row:
                return None
            result = [[0 for _ in range(other.column)] for _ in range(self.row)]
            for i in range(self.row):
                for j in range(other.column):
                    for k in range(self.column):
                        result[i][j] += self.elements[i][k] * other.elements[k][j]
            return Matrix(result)

        # Matrix × Vector
        elif isinstance(other, Vector) and self.row == 3 and self.column == 3:
            x = self.elements[0][0] * other.x + self.elements[0][1] * other.y + self.elements[0][2] * other.z
            y = self.elements[1][0] * other.x + self.elements[1][1] * other.y + self.elements[1][2] * other.z
            z = self.elements[2][0] * other.x + self.elements[2][1] * other.y + self.elements[2][2] * other.z
            return Vector(x, y, z)

        else:
            return None

    def __truediv__(self,m2):
        if m2.inverse() == None:
            return None
        else:
            return self * m2.inverse()
        
    def inverse2x2(self):
        a = self.elements[0][0]
        b = self.elements[0][1]
        c = self.elements[1][0]
        d = self.elements[1][1]
        det = (a*d)-(b*c)
        if det != 0:
            m3 = Matrix.zero(self.row, self.column)
            m3.elements[0][0] = d/det
            m3.elements[0][1] = -b/det
            m3.elements[1][0] = -c/det
            m3.elements[1][1] = a/det
            return m3
        else:
            return None
    
    def inverse3x3(self):
        a = self.elements[0][0]
        b = self.elements[0][1]
        c = self.elements[0][2]
        d = self.elements[1][0]
        e = self.elements[1][1]
        f = self.elements[1][2]
        g = self.elements[2][0]
        h = self.elements[2][1]
        i = self.elements[2][2]
        det = (a*(e*i-f*h))-(b*(d*i-f*g))+(c*(d*h-e*g))
        if det != 0:
            m3 = Matrix.zero(self.row, self.column)
            m3.elements[0][0] = (e*i-f*h)/det
            m3.elements[0][1] = (c*h-b*i)/det
            m3.elements[0][2] = (b*f-c*e)/det
            m3.elements[1][0] = (f*g-d*i)/det
            m3.elements[1][1] = (a*i-c*g)/det
            m3.elements[1][2] = (c*d-a*f)/det
            m3.elements[2][0] = (d*h-e*g)/det
            m3.elements[2][1] = (b*g-a*h)/det
            m3.elements[2][2] = (a*e-b*d)/det
            return m3
        else:
            return None
    
    def inverse(self):
        if self.row == self.column:
            if self.row == 2:
                m3 = self.inverse2x2()
            elif self.row == 3:
                m3 = self.inverse3x3()
            else:
                return None
            return m3
        else:
            return None        

    

    def get_combined_rotation_matrix(rotation_angle_vector):
        rx = rotation_angle_vector.x
        ry = rotation_angle_vector.y
        rz = rotation_angle_vector.z

        # Rotation around X-axis
        Rx = Matrix([
            [1, 0, 0],
            [0, math.cos(rx), -math.sin(rx)],
            [0, math.sin(rx), math.cos(rx)]
        ])

        # Rotation around Y-axis
        Ry = Matrix([
            [math.cos(ry), 0, math.sin(ry)],
            [0, 1, 0],
            [-math.sin(ry), 0, math.cos(ry)]
        ])

        # Rotation around Z-axis
        Rz = Matrix([
            [math.cos(rz), -math.sin(rz), 0],
            [math.sin(rz), math.cos(rz), 0],
            [0, 0, 1]
        ])

        # Combine: R = Rz * Ry * Rx
        
        return Rz * Ry * Rx


    def rotate_vector(vec, matrix):
        vec_m = Matrix([[vec.x], [vec.y], [vec.z]])
        result = matrix * vec_m
        return Vector(result.elements[0][0], result.elements[1][0], result.elements[2][0])

class Ray():
    def __init__(self, origin, direction):
        self.origin = (origin)
        self.direction = (direction).norm()

    def __str__(self):
        print(self.origin)
        print(self.direction)
    
    def point(self,t):
        return (self.origin) + (self.direction * t)




