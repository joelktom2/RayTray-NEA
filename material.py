import math
from image import colour
class material():
    def __init__(self, colour, diffuse,specular, ambient, reflectivity=0.0,texture = None):
        self.colour = colour  # Colour of the material
        self.specular = specular 
        self.diffuse = diffuse  
        self.ambient = ambient  
        self.reflectivity = reflectivity
        self.texture = texture

    def get_colour(self,point):
        if self.texture == None:
            return self.colour
        else:
            return self.texture.get_colour(point)


class checker_texture:
    def __init__(self, colour1=colour(1,0,0), colour2=colour(0,0,1), scale=1):
        self.colour1 = colour1
        self.colour2 = colour2
        self.scale = scale

    def get_colour(self, point):
        x = point.x
        y = point.y
        z = point.z
        checker = (math.floor(x * self.scale) + math.floor(y * self.scale) + math.floor(z * self.scale)) % 2
        
        if checker == 0:
            return self.colour1
        else:
            return self.colour2
        