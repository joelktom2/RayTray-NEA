class Scene():
    def __init__(self,objects,camera,width,height,lights):
        self.objects = objects       # list of objects in the scene
        self.camera = camera       # camera object
        self.width = width          # width of the image
        self.height = height        # height of the image
        self.lights = lights       # list of light sources
    
        
class camera():
    def __init__(self,position):
        self.position = position    # (x,y,z) coordinates of the camera

    def __str__(self):
        return "Camera at position: " + str(self.position)