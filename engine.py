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
        normal = nearest.get_normal(i_p)   #noraml to get_normal
        normal = normal.norm()
        light = scene.lights[0]
        camera = scene.camera
        light_intensity = light.intensity_at_point(i_p)
        #light_dir = (i_p - light.position).norm()
        light_dir = (light.position - i_p).norm()
        
        ##print(f"light dir : {light_dir}")
        ##print(normal)
        return engine.Blinn_Phong(base_colour,light_intensity,normal,i_p,light_dir,nearest,camera)       #returns the colour of the object at the point of intersection
    
    def lamb(light_intensity,normal,light_dir,diffuse):
        #print(f"base : {base_colour}")
        #print(f"i : {light.intensity_at_point(i_p)}")
        #print(f"max : {max(0,(light_dir).dp(normal))}")
        return diffuse * light_intensity * max(0,(light_dir).dp(normal)) #returns the lambertian shading of the object
    
    def specular(light_intensity,normal,halfway,specular):
        return specular * light_intensity * (max(0, halfway.dp(normal)) ** specular)
    
    
    def ambient(light_intesity,ambient):
        return ambient * light_intesity

    def Blinn_Phong(base_colour,light_intensity,normal,i_p,light_dir,nearest,camera):
        specular = nearest.material.specular
        ambient = nearest.material.ambient
        diffuse = nearest.material.diffuse
        
        
        normal = normal.norm()
        view_dir = (camera.position - i_p).norm()
        halfway = (light_dir + view_dir).norm()
        
        def clamp(value, min_val, max_val):
            return max(min_val, min(value, max_val))
        
        ambient_intensity = engine.ambient(light_intensity,ambient)
        diffuse_intensity = engine.lamb(light_intensity,normal,light_dir,diffuse)
        specular_intensity = engine.specular(light_intensity,normal,halfway,specular)
        
        ambient_intensity = clamp(ambient_intensity,0,1)
        diffuse_intensity = clamp(diffuse_intensity,0,1)
        specular_intensity = clamp(specular_intensity,0,1)


        return base_colour * (ambient_intensity + diffuse_intensity + specular_intensity)

    
    
    def ray_trace(self,ray,scene):
        fcolour = colour(0,0,0) #defualt colour : black
        
        object_hit,intersect_point = self.nearest(scene,ray)
        
        if object_hit != None:
            #print((object_hit.colour))
            pass
        
        if object_hit == None or intersect_point == None:
            return fcolour
        
                
        fcolour = self.color_at(scene,object_hit,intersect_point) # returns the colour of the object at the point of intersection
        #print(fcolour)
        
        # if object_hit:
        #     print(fcolour)
        
        return fcolour
        
        