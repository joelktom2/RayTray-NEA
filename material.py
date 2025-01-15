class material():
    def __init__(self, color, specular=0.5, diffuse=0.0, ambient=0.0):
        self.color = color  # Color of the material
        self.specular = specular  # Specular shininess
        self.diffuse = diffuse  # Reflectivity of the surface
        self.ambient = ambient  # Transparency level