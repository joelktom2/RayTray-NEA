from image import colour
class light():
    def __init__(self,position,colour= colour(1,1,1),brightness=1.0):
        self.position = position
        self.colour = colour
        self.intesity = brightness
        self.on = False
    
    def intensity_at_point(self,point):
        d = (point - self.position).mag()
        return self.intesity/((0.01*(d**2))+(0.1*d)+1)
    
    def set_color(self, color):
        self.color = color

    def set_brightness(self, brightness):
        self.brightness = brightness

    def __str__(self):
        print(f" {self.on}, {self.color}, {self.brightness}") 