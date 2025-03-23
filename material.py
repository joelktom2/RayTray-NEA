
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


    def values(self):
        return [self.diffuse, self.specular, self.ambient, self.reflectivity]