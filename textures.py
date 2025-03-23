from image import colour
import math

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
        
    
        


class GradientTexture:
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
    

