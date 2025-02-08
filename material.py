class material():
    def __init__(self, color, diffuse,specular, ambient, reflectivity=0.0):
        self.color = color  # Color of the material
        self.specular = specular 
        self.diffuse = diffuse  
        self.ambient = ambient  
        self.reflectivity = reflectivity