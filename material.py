class material():
    def __init__(self, color, shininess=0.5, reflectivity=0.0, transparency=0.0):
        self.color = color  # Color of the material
        self.shininess = shininess  # Specular shininess
        self.reflectivity = reflectivity  # Reflectivity of the surface
        self.transparency = transparency  # Transparency level