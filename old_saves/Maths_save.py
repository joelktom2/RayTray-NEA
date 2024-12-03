import math
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
    
class Matrix():
    def __init__(self,elements):

        self.row = len(elements)
        self.column = len(elements[0])
        self.elements = elements
    
    def __str__(self):
        return f"{self.elements}"
    
    def __add__(self,m2):
        if self.row == m2.row and self.column == m2.column:
            m3 = Matrix([[0 for _ in range(self.column)] for _ in range(self.row)])
            for x in range(self.row):
                for y in range(self.column):
                    m3.elements[x][y] = self.elements[x][y] + m2.elements[x][y]
        
            return m3
        else:
            return None
        
    def __sub__(self,m2):
        
        if self.row == m2.row and self.column == m2.column:
            m3 = Matrix([[0 for _ in range(self.column)] for _ in range(self.row)])
            for x in range(self.row):
                for y in range(self.column):
                    m3.elements[x][y] = self.elements[x][y] - m2.elements[x][y]
        
            return m3
        else:
            return None
    
    def __mul__(self,m2):
        m3 = Matrix([[0 for _ in range(self.column)] for _ in range(self.row)])
        if self.column == m2.row:
            for x in range(len(self.elements)):  
                for j in range(m2.column):    
                    total = 0
                    for i in range(self.column):  
                        total += self.elements[x][i] * m2.elements[i][j]
                    print(total)
                    print(f"x : {x} j: {j}")
                    m3.elements[x][j] = total
            return m3
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
            m3 = Matrix([[0 for _ in range(self.column)] for _ in range(self.row)])
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
            m3 = Matrix([[0 for _ in range(self.column)] for _ in range(self.row)])
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
    
    def inverse4x4(self):
        pass
    
    def inverse(self):
        if self.row == self.column:
            if self.row == 2:
                m3 = self.inverse2x2()
            elif self.row == 3:
                m3 = self.inverse3x3()
            elif self.row == 4:
                m3 = self.inverse4x4()
            else:
                return None
            return m3
        else:
            return None        

class Ray():
    def __init__(self, origin, direction):
        self.origin = (origin)
        self.direction = (direction)

    def __str__(self):
        print(self.origin)
        print(self.direction)
    
    def point(self,t):
        return (self.origin) + (self.direction * t)



def refract(n1, n2, normal, incident):   #random 
    incident_angle = incident.angle(normal)
    refracted_angle = math.asin((n1*math.sin(incident_angle))/n2) #applies snell's law
    return refracted_angle 