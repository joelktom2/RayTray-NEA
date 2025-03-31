from image import colour
import math
import random

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
            
class gradient_texture:
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
    
class noise_texture:
    def __init__(self,colour1=colour(1, 1, 1), colour2=colour(0, 0, 0),):
        self.noise_generator = ValueNoise3D(grid_size=32)
        self.colour1 = colour1
        self.colour2 = colour2
        self.scale = 5

    def get_colour(self, point):
        x = point.x * self.scale
        y = point.y * self.scale
        z = point.z * self.scale
        
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

# class wood_texture(self, point):
#     self.noise_generator = ValueNoise3D(grid_size=32)
#     noise_value = self.noise_generator.noise(point.x * self.scale, point.y * self.scale, point.z * self.scale)
#     grain = 0.5 * (1 + math.sin((point.x + point.y + point.z) * self.scale + noise_value * 10))
#     return colour(
#         (1 - grain) * self.colour1.x + grain * self.colour2.x,
#         (1 - grain) * self.colour1.y + grain * self.colour2.y,
#         (1 - grain) * self.colour1.z + grain * self.colour2.z
#     )

class wood_texture():
    def __init__(self, colour1=colour(0.8, 0.6, 0.3), colour2=colour(0.6, 0.4, 0.2)):
        self.noise_generator = ValueNoise3D(grid_size=32)
        self.colour1 = colour1
        self.colour2 = colour2
        self.scale = 10
        
    def get_colour(self, point):
        
        noise_value = self.noise_generator.noise(point.x * self.scale, point.y * self.scale, point.z * self.scale)
        grain = 0.5 * (1 + math.sin((point.x + point.y + point.z) * self.scale + noise_value * 10))

        return colour(
            (1 - grain) * self.colour1.x + grain * self.colour2.x,
            (1 - grain) * self.colour1.y + grain * self.colour2.y,
            (1 - grain) * self.colour1.z + grain * self.colour2.z
        )
    
class marble_texture():
    def __init__(self,colour1=colour(0.95, 0.95, 0.95),colour2=colour(0.6, 0.6, 0.6)):
        self.noise_generator = ValueNoise3D(grid_size=32)
        self.colour1 = colour1
        self.colour2 = colour2
        self.scale = 1
        
    def get_colour(self, point):
        
        turbulence = 0.0
        scale = self.scale
        for i in range(5):
            turbulence += abs(self.noise_generator.noise(point.x * scale, point.y * scale, point.z * scale)) / scale
            scale *= 2
        t = 0.5 * (1 + math.sin(point.x * self.scale + turbulence * 5))
        return colour(
            (1 - t) * self.colour1.x + t * self.colour2.x,
            (1 - t) * self.colour1.y + t * self.colour2.y,
            (1 - t) * self.colour1.z + t * self.colour2.z
        )
    
class cloud_texture():
    def __init__(self, colour1=colour(1, 1, 1), colour2=colour(0.8, 0.8, 0.8)):
        self.noise_generator = ValueNoise3D(grid_size=32)
        self.colour1 = colour1
        self.colour2 = colour2
        self.scale = 5
        
    def get_colour(self, point):
        
        noise_value = self.noise_generator.noise(point.x * self.scale, point.y * self.scale, point.z * self.scale)
        t = (noise_value + 1) / 2
        t = max(0, min(1, t))
        return colour(
            (1 - t) * self.colour1.x + t * self.colour2.x,
            (1 - t) * self.colour1.y + t * self.colour2.y,
            (1 - t) * self.colour1.z + t * self.colour2.z
        )