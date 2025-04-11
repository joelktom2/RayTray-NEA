class Scene():
    def __init__(self,objects,camera,width,height,lights):
        self.objects = objects       # list of objects in the scene
        self.camera = camera       # camera object
        self.width = width          # width of the image
        self.height = height        # height of the image
        self.lights = lights       # list of light sources
    def __str__(self):
        obj1 = self.objects[0]
        obj2 = self.objects[1]
        return f"Camera at position: {self.camera.position} Width: {self.width} Height: {self.height} obj 1 pos :{obj1.center}, obj 2 pos :{obj2.center},"

class camera():
    def __init__(self,position,fov= 90):
        self.position = position    # (x,y,z) coordinates of the camera
        self.fov = fov

    def __str__(self):
        return "Camera at position: " + str(self.position)