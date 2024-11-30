from Maths import Vector
from scene import Scene
from objects import camera
from objects import Sphere
from image import colour



width = 300
height = 200
myobj = Sphere(Vector(0, 0, 5), 0.5, colour(1,0,0))
mycam = camera(Vector(0, 0, -1))
scene = Scene([myobj],mycam,width,height)
user_scene = Scene([myobj],mycam,width,height)  

print("#################")
print(user_scene.camera)
print(user_scene.camera.position)
print(user_scene.objects)
print(user_scene.objects[0].center)
print(user_scene.width)
print(user_scene.height)