from Maths import Vector
from scene import Scene
from objects import camera
from objects import Sphere
from image import colour
from engine import engine

def main(user_scene):

    Engine = engine()
    image = Engine.render(user_scene)
    with open("image.ppm", "w") as img_file:
        image.write_ppm(img_file)

#initialized variables for scene ,constant for simplicity for now
width = 300
height = 200
myobj = Sphere(Vector(0, 0, 5), 0.5, colour(1,0,0))
mycam = camera(Vector(0, 0, -1))
scene = Scene([myobj],mycam,width,height)
user_scene = Scene([myobj],mycam,width,height)  

def main(user_scene):

    Engine = engine()
    image = Engine.render(user_scene)
    with open("good.ppm", "w") as img_file:
        image.write_ppm(img_file)

main(user_scene)


