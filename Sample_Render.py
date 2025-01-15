from Maths import Vector
from scene import Scene,camera
from objects import Sphere
from image import colour
from engine import engine
from light import light
import cv2
import matplotlib.pyplot as plt
from objects import Plane

def render(file):    
    img = cv2.imread(file)
    img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    plt.imshow(img)
    plt.show()


def main(user_scene):

    Engine = engine()
    image = Engine.render(user_scene)
    with open("image.ppm", "w") as img_file:
        image.write_ppm(img_file)

#initialized variables for scene ,constant for simplicity for now
width = 300
height = 200
myobj = Sphere(Vector(0, 0, 4), 2.0, colour(1,0,0),[0.8, 0.5, 0.2])


mycam = camera(Vector(0, -0.35, -1))
s1 = Sphere(Vector(0,0,2), 0.5, colour(0,1,0))
p1 = Plane(Vector(0,3,0),Vector(0,-1,0))
ls = Sphere(Vector(0,10000.5,1), 10000, colour(0,0,1))

objects = []
objects.append(myobj)

l1 = light(Vector(0,0,1),colour(1,1,1)) 

user_scene = Scene(objects,mycam,width,height,[l1])  

main(user_scene)
render("image.ppm")




