from Maths import Vector 
class colour(Vector):
    
    def hex_to_rgb(hex):
        hex = hex.lstrip('#')
        r = int(int(hex[0:2], 16)/255)
        g = int(int(hex[2:4], 16)/255)
        b = int(int(hex[4:6], 16)/255)
        return colour(r, g, b)

    


class Image:      
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.pixels = [[0 for x in range(width)] for y in range(height)]  

    def set_pixel(self, x, y, color):
        self.pixels[y][x] = color

    def write_ppm(self, file):
        
        
        file.write("P3\n")
        file.write(f"{self.width} {self.height}\n")
        file.write("255\n")
        for row in self.pixels:
            for pixel in row:
                file.write(f"{pixel.x*255} {pixel.y*255} {pixel.z*255}\n")



