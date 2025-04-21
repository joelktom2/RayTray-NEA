from image import colour
import math
import random
from Maths import Vector
from PIL import Image

class Texture:
    def __init__(self):
        pass

    def get_colour(self, point):
        raise NotImplementedError("Subclasses must implement a get_colour method.")

class checker_texture(Texture):
    def __init__(self, colour1=colour(1,0,0), colour2=colour(0,0,1)):
        self.colour1 = colour1
        self.colour2 = colour2
        

    def get_colour(self, point):
        scale =1 
        x = point.x
        y = point.y
        z = point.z
        checker = (math.floor(x * scale) + math.floor(y * scale) + math.floor(z * scale)) % 2
        
        if checker == 0:
            return self.colour1
        else:
            return self.colour2
            
class gradient_texture(Texture):
    def __init__(self, color_start=colour(1, 0, 0), color_end=colour(0, 0, 1)):
        self.color_start = color_start
        self.color_end = color_end

    def get_colour(self, point):
        t = (point.y*0.2 + 1) / 2  # Normalize y-coordinate to [0,1]
        t = max(0, min(1, t))
        return colour(
            (1 - t) * self.color_start.x + t * self.color_end.x,
            (1 - t) * self.color_start.y + t * self.color_end.y,
            (1 - t) * self.color_start.z + t * self.color_end.z,
        )
    
class noise_texture(Texture):
    def __init__(self,colour1=colour(1, 1, 1), colour2=colour(0, 0, 0)):
        self.noise_generator = ValueNoise3D(grid_size=32)
        self.colour1 = colour1
        self.colour2 = colour2
        

    def get_colour(self, point):
        scale = 5
        x = point.x * scale
        y = point.y * scale
        z = point.z * scale
        
        # Generate noise value in the range [-1, 1]
        noise_value = self.noise_generator.noise(x, y, z)
        
        # Remap noise value from [-1, 1] to [0, 1]
        t = (noise_value + 1) / 2
        
        # Interpolate between colour1 and colour2 based on noise
        return colour(
            (1 - t) * self.colour1.x + t * self.colour2.x,
            (1 - t) * self.colour1.y + t * self.colour2.y,
            (1 - t) * self.colour1.z + t * self.colour2.z
        )

# Fade function for smooth interpolation
def fade(t):
    return t * t * t * (t * (t * 6 - 15) + 10)

# Linear interpolation
def lerp(a, b, t):
    return a + t * (b - a)

class ValueNoise3D:
    def __init__(self, grid_size=16, seed=42):
        self.grid_size = grid_size
        self.seed = seed
        random.seed(seed)
        self.grid = self.generate_grid()

    def generate_grid(self):
        # Generate a random value at each grid point
        return {(x, y, z): random.uniform(-1, 1) 
                for x in range(self.grid_size)
                for y in range(self.grid_size)
                for z in range(self.grid_size)}

    def get_gradient(self, x, y, z):
        # Wrap coordinates using modulo for seamless tiling
        return self.grid[(x % self.grid_size, y % self.grid_size, z % self.grid_size)]

    def noise(self, x, y, z):
        # Grid cell coordinates
        x0 = int(math.floor(x))
        y0 = int(math.floor(y))
        z0 = int(math.floor(z))
        x1 = x0 + 1
        y1 = y0 + 1
        z1 = z0 + 1

        # Fractional part within the cell
        sx = x - x0
        sy = y - y0
        sz = z - z0

        # Get noise values from cube corners
        n000 = self.get_gradient(x0, y0, z0)
        n001 = self.get_gradient(x0, y0, z1)
        n010 = self.get_gradient(x0, y1, z0)
        n011 = self.get_gradient(x0, y1, z1)
        n100 = self.get_gradient(x1, y0, z0)
        n101 = self.get_gradient(x1, y0, z1)
        n110 = self.get_gradient(x1, y1, z0)
        n111 = self.get_gradient(x1, y1, z1)

        # Apply fade function for smooth interpolation
        u = fade(sx)
        v = fade(sy)
        w = fade(sz)

        # Perform trilinear interpolation
        nx00 = lerp(n000, n100, u)
        nx01 = lerp(n001, n101, u)
        nx10 = lerp(n010, n110, u)
        nx11 = lerp(n011, n111, u)

        nxy0 = lerp(nx00, nx10, v)
        nxy1 = lerp(nx01, nx11, v)

        return lerp(nxy0, nxy1, w)


class wood_texture(Texture):
    def __init__(self, colour1=colour(0.8, 0.6, 0.3), colour2=colour(0.6, 0.4, 0.2)):
        self.noise_generator = ValueNoise3D(grid_size=32)
        self.colour1 = colour1
        self.colour2 = colour2
        
        
    def get_colour(self, point):
        scale = 10
        noise_value = self.noise_generator.noise(point.x * scale, point.y * scale, point.z * scale)
        grain = 0.5 * (1 + math.sin((point.x + point.y + point.z) * scale + noise_value * 10))

        return colour(
            (1 - grain) * self.colour1.x + grain * self.colour2.x,
            (1 - grain) * self.colour1.y + grain * self.colour2.y,
            (1 - grain) * self.colour1.z + grain * self.colour2.z
        )
    
class marble_texture(Texture):
    def __init__(self,colour1=colour(0.95, 0.95, 0.95),colour2=colour(0.6, 0.6, 0.6)):
        self.noise_generator = ValueNoise3D(grid_size=32)
        self.colour1 = colour1
        self.colour2 = colour2
        
        
    def get_colour(self, point):
        
        turbulence = 0.0
        scale = 1
        for i in range(5):
            turbulence += abs(self.noise_generator.noise(point.x * scale, point.y * scale, point.z * scale)) / scale
            scale *= 2
        t = 0.5 * (1 + math.sin(point.x * scale + turbulence * 5))
        return colour(
            (1 - t) * self.colour1.x + t * self.colour2.x,
            (1 - t) * self.colour1.y + t * self.colour2.y,
            (1 - t) * self.colour1.z + t * self.colour2.z
        )
    
class smoke_texture(Texture):
    def __init__(self, colour1=colour(1, 1, 1), colour2=colour(0.8, 0.8, 0.8)):
        self.noise_generator = ValueNoise3D(grid_size=32)
        self.colour1 = colour(1, 1, 1)
        self.colour2 = colour(0.8, 0.8, 0.8)
        
        
    def get_colour(self, point):
        scale = 5
        noise_value = self.noise_generator.noise(point.x * scale, point.y * scale, point.z * scale)
        t = (noise_value + 1) / 2
        t = max(0, min(1, t))
        return colour(
            (1 - t) * self.colour1.x + t * self.colour2.x,
            (1 - t) * self.colour1.y + t * self.colour2.y,
            (1 - t) * self.colour1.z + t * self.colour2.z
        )
    
class stripes_texture(Texture):
    def __init__(self, colour1=colour(1, 1, 1), colour2=colour(0, 0, 0)):
        self.colour1 = colour1
        self.colour2 = colour2
    
    def get_colour(self, point):
        scale = 10  # Adjust this value to change the stripe width
        coord = point.x 
        if int(math.floor(coord * scale)) % 2 == 0:
            return self.colour1
        else:
            return self.colour2
        
class radial_texture(Texture):
    def __init__(self, colour1=colour(1, 1, 1), colour2=colour(0, 0, 0)):
        self.colour1 = colour1
        self.colour2 = colour2
        
   

    def get_colour(self, point):
        center = Vector(0,0,0)
        scale = 1
        center_to_point = point - center
        dist = center_to_point.mag() * scale
        
        # Normalize the distance to [0, 1]
        t = min(1, max(0, dist))
        return colour(
            (1 - t) * self.colour1.x + t * self.colour2.x,
            (1 - t) * self.colour1.y + t * self.colour2.y,
            (1 - t) * self.colour1.z + t * self.colour2.z
        )
    

class brick_texture(Texture):
    def __init__(self, brick_colour=colour(0.7, 0.2, 0.1), mortar_colour=colour(0.85, 0.85, 0.85), ):
        self.colour1 = brick_colour # Brick colour
        self.colour2 = mortar_colour

    def get_colour(self, point):
        brick_width = 1
        brick_height = 0.5
        mortar_thickness = 0.05
        
        x = point.x
        y = point.y

        # Determine the current row and column
        row = math.floor(y / brick_height)
        offset = 0.5 * brick_width if row % 2 == 1 else 0  # Stagger every other row

        

        # Local position inside the brick
        local_x = (x + offset) % brick_width
        local_y = y % brick_height

        # If near the edge, it's mortar
        if (local_x < mortar_thickness or local_y < mortar_thickness or 
            local_x > brick_width - mortar_thickness or 
            local_y > brick_height - mortar_thickness):
            return self.colour2  # Mortar colour
        else:
            return self.colour1  # Brick colour
        


class image_texture(Texture):
    def __init__(self, image_path):
        self.image = self.load_image(image_path)
        self.width, self.height = self.image.size
        self.pixels = self.image.load()

    def load_image(self, image_path):
        # Load and convert image to RGB
        return Image.open(image_path).convert("RGB")

    def get_colour(self, point):
        # Map point coordinates to [0,1] UV space
        # You can adapt this projection based on your scene layout
        u = (point.x % 1 + 1) % 1  # Wrap around
        v = (point.y % 1 + 1) % 1

        # Flip v because image Y-axis is top-down
        v = 1 - v

        # Convert UV to image coordinates
        x_pixel = int(u * (self.width - 1))
        y_pixel = int(v * (self.height - 1))

        r, g, b = self.pixels[x_pixel, y_pixel]

        # Normalize RGB to [0,1]
        return colour(r / 255, g / 255, b / 255)
