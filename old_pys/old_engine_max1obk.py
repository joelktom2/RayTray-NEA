from image import colour
from image import Image
from Maths import Ray,Vector

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

        camera = scene.camera
        pixels = Image(width, height)
        
        for j in range(height):
            y = y_min + j * ystep  #y coord
            for i in range(width):
                x = x_min + i * xstep #x coord
                ray = Ray(camera.position, (Vector(x, y, 0)- camera.position).norm())       #essentiall produces a ray in the direction of the pixels
                pixels.set_pixel(i, j, self.ray_trace(ray,scene))
        
        return pixels
    
    def nearest(self,scene,ray):
        cam = scene.camera.position
        d = 0
        nearest = None
        for x in scene.objects:
            (scene.camera).position = cam
            i_p = x.intersects(ray)
            if i_p == None:
                return None,i_p
            nd = (cam - i_p).mag
            if d == 0:
                nd = d
                nearest = x
            elif nd < d:
                d = nd
                nearest = x
        return nearest,i_p
    
    def color_at(self,scene,ray,nearest,i_p):
        return nearest.colour
    
    def ray_trace(self,ray,scene):
        fcolour = colour(0,0,0) #defualt colour : plain red
        
        object_hit,intersect_point = self.nearest(scene,ray)
        
       
        
        if object_hit == None:
            return fcolour
        
        fcolour += self.color_at(scene,ray,object_hit,intersect_point)
  
        return fcolour
        
        