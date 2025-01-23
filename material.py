class material():
    def __init__(self, color, diffuse=0.5,specular=0.5, ambient=0.0, reflectivity=0.0):
        self.color = color  # Color of the material
        self.specular = specular 
        self.diffuse = diffuse  
        self.ambient = ambient  
        self.reflectivity = reflectivity