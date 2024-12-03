from image import colour
class light():
    def __init__(self,colour= colour(1,1,1),brightness=1.0):
        self.name = "light"
        self.colour = colour
        self.intesity = brightness
        self.on = False

    def on(self):
        self.on = True

    def off(self):
        self.on = False

    def set_color(self, color):
        self.color = color

    def set_brightness(self, brightness):
        self.brightness = brightness

    def get_state(self):
        return self.on, self.color, self.brightness