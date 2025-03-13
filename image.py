from Maths import Vector 
class colour(Vector):
    
    def hex_to_rgb(hex):         # converts hex colour to rgb colour
       
        if hex == None:
            return None
        hex = hex.lstrip('#')
        
        r = int(int(hex[0:2], 16)/255)
        g = int(int(hex[2:4], 16)/255)
        b = int(int(hex[4:6], 16)/255)
        return colour(r, g, b)
    
    
    


class Image:      
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.pixels = [[0 for x in range(width)] for y in range(height)]  # 2D list of pixels in the image

    def set_pixel(self, x, y, color):
        self.pixels[y][x] = color    # sets the colour of a pixel at (x,y) in the image

    def write_ppm(self, file):
        
        # writes the image to a ppm file using the pixel map
        file.write("P3\n")
        file.write(f"{self.width} {self.height}\n")
        file.write("255\n")
        for row in self.pixels:
            for pixel in row:
                file.write(f"{int(pixel.x*255)} {int(pixel.y*255)} {int(pixel.z*255)}\n")



