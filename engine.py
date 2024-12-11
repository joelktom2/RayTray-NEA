from image import colour
from image import Image
from Maths import Ray,Vector
from light import light
class engine:
    

    def render(self,scene):
    
        width = scene.width
        height = scene.height        
        
        ar = width / height     
        y_max = 1 /  ar
        y_min = -y_max
        x_max = 1.0
        x_min = -x_max
        xstep = (x_max - x_min) / (width - 1)
        ystep = (y_max - y_min) / (height - 1)

        #lines 13 -19 are used to avoid image distortion by keeping the aspect ratio of the image constant
        camera = scene.camera
        pixels = Image(width, height)
        #loop through each pixel in the image and traces a ray through it
        for j in range(height):
            y = y_min + j * ystep  #y coord
            for i in range(width):
                x = x_min + i * xstep #x coord
                ray = Ray(camera.position, (Vector(x, y, 0)- camera.position).norm())       #essentiall produces a ray in the direction of the pixels
                pixels.set_pixel(i, j, (self.ray_trace(ray,scene)))
        
        return pixels
    
    def nearest(self,scene,ray):
        cam = scene.camera.position
        d = 0
        nearest = None
        nearesti_p = None
        for x in scene.objects:   #loops through all the objects in the scene and finds the nearest object to the camera
            (scene.camera).position = cam
            i_p = x.intersects(ray)
            if i_p == None:
                continue
            nd = (cam - i_p).mag
            if d == 0:
                d = nd
                nearest = x
                nearesti_p = i_p
            elif nd < d:
                d = nd
                nearest = x
                nearesti_p = i_p

        return nearest,nearesti_p  #returns the object that the ray intersects with and the point of intersection
    
    def color_at(self,scene,nearest,i_p):
        base_colour = nearest.colour
        normal = nearest.normal(i_p)
        light = scene.lights[0]
        light_dir = (light.position - i_p).norm()
        return engine.lamb(base_colour,light,normal,i_p,light_dir) #returns the colour of the object at the point of intersection
    
    def lamb(base_colour,light,normal,i_p,light_dir):
        return base_colour * light.intensity_at_point(i_p) * max(0,(light_dir).dp(normal)) #returns the lambertian shading of the object
    

    
    def ray_trace(self,ray,scene):
        fcolour = colour(0,0,0) #defualt colour : black
        
        object_hit,intersect_point = self.nearest(scene,ray)
        if object_hit != None:
            print((object_hit.colour))
        
        if object_hit == None:
            return fcolour
        
        if intersect_point == None:
            return fcolour
                
        fcolour = self.color_at(scene,object_hit,intersect_point) # returns the colour of the object at the point of intersection
        print(fcolour)
        return fcolour
        
        