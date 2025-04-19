from Maths import Vector
from scene import Scene,camera
from objects import Sphere , Cone,Ellipsoid,Cylinder,Floor,Cube,Tetrahedron,Capsule
from image import colour
from engine import engine
from light import light
import cv2
import matplotlib.pyplot as plt

from material import material
from textures import *
import math

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

myobj = Sphere(Vector(0, 0, 5), 1.5, colour(0,0,1),[0.6,0.2,0.2,0.4])   #low reflection val dont work now


mycam = camera(Vector(0, 0, -1),120)


s1 = Sphere(Vector(0,0,5), 2.5, colour(0,0,1),[0.5,0.5,0.0,0.0])

ls = Sphere(Vector(0,10000.5,1), 10000, None,[0.5,0.5,0.0,0.0],gradient_texture())
c1 = Cone(Vector(0,-5.5,5),Vector(0,1,0),math.pi/6,5,colour(1,0,0),[0.5,0.5,0.0,0.0])
e1 = Ellipsoid(Vector(0,0,5),Vector(3,50,3),colour(0,1,0),[0.5,0.5,0.0,0.0],checker_texture())
cy1 = Cylinder(Vector(0,-2,5),"x",2,1,colour(1,0,0),[0.5,0.5,0.0,0.0],gradient_texture())
f1 = Floor(colour(0,0,0),[0.5,0.5,0.0,0.0],checker_texture())
#cube1 = Cube(Vector(-2,0,3),2,colour(1,0,0),[0.5,0.5,0.0,0.0],checker_texture())
capsule1 = Capsule(Vector(0,0,5),"y",6,1,colour(1,0,0),[0.5,0.5,0.0,0.0])
rcube = Cube(Vector(0,0,3),2,Vector(0, math.radians(30), 0),colour(1,0,0),[0.5,0.5,0.0,0.0],checker_texture())
t1 = Tetrahedron(Vector(-8,0,5),3,colour(1,0,0),[0.5,0.5,0.0,0.0])
objects = []
objects.append(capsule1)




l1 = light(Vector(0,0,0),colour(1,1,1)) 

user_scene = Scene(objects,mycam,width,height,[l1])  

main(user_scene)
render("image.ppm")




