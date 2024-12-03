class Scene():
    def __init__(self,objects,camera,width,height,lights):
        self.objects = objects
        self.camera = camera
        self.width = width
        self.height = height
        self.lights = lights
    
        
class camera():
    def __init__(self,position):
        self.position = position