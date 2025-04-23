from image import colour
from image import Image
from Maths import Ray,Vector
import math

MAX_DEPTH = 3
BG_COLOR = colour(0,0,0) #default background colour : black

class engine:
    

    def render(self,scene,progress_callback=None):
    
        width = scene.width
        height = scene.height        
        ar = width / height

        fov = math.radians(scene.camera.fov)  #fov in radians
        scale = math.tan(fov / 2)


        y_max = scale
        y_min = -y_max
        x_max = scale * ar
        x_min = -x_max
        
        xstep = (x_max - x_min) / (width - 1)
        ystep = (y_max - y_min) / (height - 1)

        #Above lines are used to avoid image distortion by keeping the aspect ratio of the image constant
        
        camera = scene.camera
        pixels = Image(width, height)
        
        #loop through each pixel in the image and traces a ray through it
        for j in range(height):
            y = y_max - j * ystep  
            for i in range(width):
                x = x_min + i * xstep 
                # Ray production 
                camera_direction = Vector(0,1,0) + Vector(1,0,0) * x + Vector(0,0,1) * y 
                # camera is set to look in the positive y direction.
                camera_direction = camera_direction.norm() 
                ray = Ray(camera.position, camera_direction)   

                pixels.set_pixel(i, j, (self.ray_trace(ray,scene)))
            if progress_callback:
                progress_callback((j+1 )/ height)    #for progress bar in UI
        
        return pixels
    
    def ray_trace(self,ray,scene,depth = 0):
         
        fcolour = BG_COLOR #defualt colour : black
        
        object_hit,intersect_point = self.nearest(scene,ray)
        
        
        if object_hit == None or intersect_point == None:
            return fcolour
        
        def clamp_colour(col):
            return colour(
                min(max(col.x, 0), 1),
                min(max(col.y, 0), 1),
                min(max(col.z, 0), 1)
            ) 
                
        fcolour += self.colour_at(scene,object_hit,intersect_point) # returns the colour of the object at the point of intersection
        
        if object_hit.material.reflectivity > 0 and depth < MAX_DEPTH:  #function is used recursively to calculate reflections
            depth += 1
            object_normal = object_hit.get_normal(intersect_point) #normal at the point of intersection
            reflected_ray_origin = intersect_point + object_normal * 0.00001 
            #Above line is used to avoid self intersection
            reflected_ray = self.reflect(ray, object_normal, reflected_ray_origin)

            fcolour += self.ray_trace(reflected_ray,scene,depth+1) * (object_hit.material.reflectivity)
            
        return clamp_colour(fcolour)
    
    def nearest(self,scene,ray): 
        #returns the nearest object that the ray intersects with and the point of intersection 
        cam = scene.camera.position
        d = 0
        nearest = None
        nearesti_p = None
        for x in scene.objects:   
            #loops through all the objects in the scene and finds the nearest object to the camera
            (scene.camera).position = cam
            i_p = x.intersects(ray)
            if i_p == None:
                continue
            nd = (cam - i_p).mag()

            
            if d == 0:
                d = nd
                nearest = x
                nearesti_p = i_p
            
            elif nd < d:
                d = nd
                nearest = x
                nearesti_p = i_p

        return nearest,nearesti_p  
    
    def colour_at(self,scene,nearest,i_p):
        
        base_colour = nearest.material.get_colour(i_p)
        f_colour = colour(0,0,0)

        normal = nearest.get_normal(i_p)   #calls the objects get_normal method to get the normal at the point of intersection
        normal = normal.norm()
        camera = scene.camera
        for light in scene.lights:  #sums the contribution of all the lights in the scene

            light_intensity = light.intensity_at_point(i_p)
            light_dir = (light.position - i_p).norm()
            intesity = engine.Blinn_Phong(light_intensity,normal,i_p,light_dir,nearest,camera)
            f_colour  +=  base_colour * intesity
        
        return f_colour     #returns the colour of the object at the point of intersection
    
    def lamb(light_intensity,normal,light_dir,diffuse):
        
        return diffuse * light_intensity * max(0,(light_dir).dp(normal)) #returns the lambertian shading of the object
    
    def specular(light_intensity,normal,halfway,specular):
        return specular * light_intensity * (max(0, halfway.dp(normal)) ** specular)
    
    
    def ambient(light_intesity,ambient):
        return ambient * 0.4 * light_intesity + 0.05

    def Blinn_Phong(light_intensity,normal,i_p,light_dir,nearest,camera):
        specular = nearest.material.specular
        ambient = nearest.material.ambient
        diffuse = nearest.material.diffuse
        
        
        normal = normal.norm()
        view_dir = (camera.position - i_p).norm()
        halfway = (light_dir + view_dir).norm()  #used to calculate the specular reflection
        
        def clamp(value, min_val, max_val):
            return max(min_val, min(value, max_val))
        
        ambient_intensity = engine.ambient(light_intensity,ambient)
        diffuse_intensity = engine.lamb(light_intensity,normal,light_dir,diffuse)
        specular_intensity = engine.specular(light_intensity,normal,halfway,specular)
        
        ambient_intensity = clamp(ambient_intensity,0,1)
        diffuse_intensity = clamp(diffuse_intensity,0,1)
        specular_intensity = clamp(specular_intensity,0,1)


        return (ambient_intensity + diffuse_intensity + specular_intensity)

    
    def reflect(self,ray,normal,point): #caclulates the reflection of the ray at the point of intersection
        d = ray.direction
        n = normal
        return Ray(point, (d - (n * 2 * d.dp(n))) )  #returns the reflected ray from the point of intersection
    
    

        
        