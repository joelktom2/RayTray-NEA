from Maths import Vector
from scene import Scene,camera
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
objects = []
objects.append(myobj)
objects.append(Sphere(Vector(10, 10, 15), 0.5, colour(0,1,0)))

user_scene = Scene(objects,mycam,width,height)  

main(user_scene)


