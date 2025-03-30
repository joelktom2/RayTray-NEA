#My libraries
from image import colour
from Maths import Vector
from objects import *
from engine import engine
from scene import Scene,camera
from light import light
from loginsys import create_user,login_user,get_user_id
from scenes_table import create_scene,get_scenes,get_scene_names,remove_scene
from object_table import save_object,load_objects,load_object
from material import material
from textures import *

#3rd part libraries
import flet as ft
from flet_contrib.color_picker import ColorPicker
from flet import FilePicker, FilePickerResultEvent
from PIL import Image
import numpy as np
import re
from time import sleep
import os
import shutil
import win32clipboard
import io
from datetime import datetime


def main(page):
    page.title = "RayTray"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    
    global User_Status  
    User_Status = None


    
    def switch_theme(e):
        if page.theme_mode == ft.ThemeMode.LIGHT:
            
            page.theme_mode = ft.ThemeMode.DARK
            theme_switch_button.label = "Dark Mode"
        else:
            page.theme_mode = ft.ThemeMode.LIGHT
            theme_switch_button.label = "Light Mode"
        page.update()
        

    theme_switch_button = ft.Switch(label="Dark Mode", on_change=switch_theme)     
    
    
    def username_sanitate(value):
        if re.fullmatch(r'[A-Za-z0-9#_]+', value):
            return True
        return False   #checks if the username is valid
    
    
    def password_sanitate(value):
        if " " in value:
            error_message.value = "Password Cannot contain blank spaces"
            error_message.visible = True    
            page.update()

        elif len(value) < 8:
            error_message.value = "Password Must be more than 7 characters"
            error_message.visible = True    
            page.update()
            return False
            
        elif not(re.search(r"[A-Z]",value)):
            error_message.value = "Password Must contain at least 1 Capital Letter"
            error_message.visible = True    
            page.update()
            return False 
        elif not(re.search(r"[\d]",value)):
            error_message.value = "Password Must contain at least 1 digit"
            error_message.visible = True    
            page.update()
            return False
        elif not(re.search(r"[!@\$%\^&\*\+#]",value)):
            error_message.value = "Password Must contain at least 1 special characters"
            error_message.visible = True    
            page.update()
            return False
        error_message.visible = False
        return True     


    def guest(e):
        global User_Status
        User_Status = False
        error_message.visible = False
        global saved_objects
        saved_objects = []
        switch_to_main_ui(e)

    def register(e):
        usern = username.value
        pwd = password.value
        
        if not usern or not pwd:
            error_message.value = "Please Enter a username or password"
            error_message.visible = True    
            page.update()
            return
        
        
        #input sanitation
        if not username_sanitate(usern):
            error_message.value = "Invalid username"
            error_message.visible = True
            page.update()
            return
        if not password_sanitate(pwd):
            return
        
        page.update()
        create_user(usern,pwd)
        
        path = f'C:/Users/jobyk/python/RayTray - NEA/User_Data/{get_user_id(usern)}' 
        if not os.path.exists(path):
            os.makedirs(path)
        
        
        
        global User_Status
        User_Status = True

        global saved_objects
        saved_objects = []

        switch_to_main_ui(e)
    
    def login(e):
        
        
        usern = str(username.value)
        pwd = str(password.value)
        
        #input sanitation
        if not usern or not pwd:
            error_message.value = "Please enter a username and password"
            error_message.visible = True
            page.update()
            return
        
        
        valid = login_user(usern,pwd)
        if valid == False:
            error_message.value = "Invalid username or password"
            error_message.visible = True
            page.update()
            return
        elif valid == None:
            error_message.value = "User not found"
            error_message.visible = True
            page.update()
            return
        
        page.update()
        global User_Status
        User_Status = True
        

        global saved_objects
        saved_objects = []
        
        switch_to_main_ui(e)   #switches to the main UI when the user logs in successfully
    
    
    def switch_to_main_ui(e):
        page_tracker = "main"
        
        error_message.visible = False
        
        global names
        if names == 7:
            pass
        
        
        # Clear the login page
        page.controls.clear()
        
        img = ft.Image(
            src=None,  # Initialize with no image source
            width=300,
            height=300,
            fit=ft.ImageFit.CONTAIN,
            visible=False,  # Hide the image initially
        )


        # UI components for the render page
        
    
        class Fancy_Button(ft.CupertinoFilledButton):
            def __init__(self, text, on_click):
                super().__init__()
                self.bgcolor = ft.colors.LIME_100
                self.color = ft.colors.GREEN_800
                self.text = text
                self.on_click = on_click
                self.visible = True        
                
        
        
        
        class MyButton(ft.ElevatedButton):
            def __init__(self, text, on_click):
                super().__init__()
                self.bgcolor = ft.colors.GREEN_100
                self.color = ft.colors.GREEN_800
                self.text = text
                self.on_click = on_click

        class Remove_ButtonLite(ft.ElevatedButton):
            def __init__(self, text, on_click):
                super().__init__()
                self.bgcolor = ft.colors.GREEN_100
                self.color = ft.colors.GREEN_800
                self.text = text
                self.on_click = on_click
                self.width = 100
                self.height = 20
                


        class R_Button(ft.ElevatedButton):
            def __init__(self, text, on_click):
                super().__init__()
                self.bgcolor = ft.colors.GREEN_100
                self.color = ft.colors.GREEN_800
                self.text = text
                self.on_click = on_click
                self.width = 500
                self.height = 50
                self.weight = ft.FontWeight.BOLD

       
        def validcoord(value):
            if re.fullmatch(r'-?\d+(\.\d+)?,-?\d+(\.\d+)?,-?\d+(\.\d+)?', value):
                return True
            return False
        
        def validradius(value):
            if re.fullmatch(r'\d+(\.\d+)?', value):
                return True
            return False
        
        def validlength(value):
            if re.fullmatch(r'\d+', value):
                return True
            return False
        
        added_objects = ft.Column(spacing=5)
        added_lights = ft.Column(spacing=5)
        added_cam = ft.Column(spacing=5)
        #scene data initialization
        scene_objects = []
        lights = []
        global scene_name
        scene_name = None


    
        
        
        def add_light(e):    # adds a light source to the scene 
            
            if validcoord(light_pos.value):
                light_error_message.visible = False
                position_parts = light_pos.value.split(",")
                x, y, z = map(int, position_parts)
                mylight = light(Vector(x, y, z),colour(1,1,1))
                lights.append(mylight)

                added_lights.controls.append(
                    ft.Row(
                        [(ft.Text(f"Position: {light_pos.value}")),Remove_ButtonLite(text="Remove", on_click=lambda e: remove_light(e, mylight))] , alignment=ft.MainAxisAlignment.CENTER
                        
                    ),
                )
                 
                page.update()
            else:
                light_error_message.value = "Please enter a light source"
                light_error_message.visible = True
                page.update()

        def remove_light(e,light):   #removes light source from the scene
            
            lnum = lights.index(light)
            lights.pop(lnum)
            added_lights.controls.pop(lnum)
            page.update()
        
        
        def add_cam(e): # adds a camera to the scene
            
            if validcoord(cam_pos.value):
                if added_cam.controls != []:
                    cam_error_message.value = "Only one camera is allowed"
                    cam_error_message.visible = True
                    page.update()
                    return
                cam_error_message.visible = False
                cam_parts = cam_pos.value.split(",")
                x, y, z = map(int, cam_parts)
                global scene_camera
                scene_camera = camera(Vector(x, y, z))
                added_cam.controls.append(
                    ft.Row(
                        [(ft.Text(f"Position: {cam_pos.value}")),Remove_ButtonLite(text="Remove", on_click=lambda e: remove_cam(e, scene_camera))] , alignment=ft.MainAxisAlignment.CENTER
                        
                    ),
                )
                page.update()
            else:
                cam_error_message.value = "Please enter a camera position"
                cam_error_message.visible = True
                page.update()

        def remove_cam(e,cam):   #removes camera from the scene
            added_cam.controls.pop(0)
            page.update()    
        
        
        def validate_inputs_for_sphere():
            if validcoord(object_position.value) == False:
                obj_error_message.value = "Please enter a valid position"
                obj_error_message.visible = True
                page.update()
                return False
        
            elif validradius(object_radius.value) == False:
                obj_error_message.value = "Please enter a valid radius"
                obj_error_message.visible = True
                page.update()
                return False
            elif colour_button.visible == True and selected_color == None:
                obj_error_message.value = "Please select a color"
                obj_error_message.visible = True
                page.update()
                return False
            return True
        
        def validate_inputs_for_floor():

            if colour_button.visible == True and selected_color == None:
                obj_error_message.value = "Please select a color"
                obj_error_message.visible = True
                page.update()
                return False
            return True
        
        def validate_inputs_for_cone():
            if validate_inputs_for_sphere() == False:
                return False
            elif validcoord(cone_axis.value) == False:
                obj_error_message.value = "Please enter a valid axis"
                obj_error_message.visible = True
                page.update()
                return False
            elif float(cone_angle.value) <=0.0 or float(cone_angle.value) >= 90.0:
                obj_error_message.value = "Please enter a valid angle between 0 and 90 degrees"
                obj_error_message.visible = True
                page.update()
                return False
            #check axis and angle
            return True
        
        
        def validate_inputs_for_Ellipsoid():
            if validcoord(object_position.value) == False:
                obj_error_message.value = "Please enter a valid position"
                obj_error_message.visible = True
                page.update()
                return False
            elif colour_button.visible == True and selected_color == None:
                obj_error_message.value = "Please select a color"
                obj_error_message.visible = True
                page.update()
                return False
            elif colour_button.visible == True and selected_color == None:
                obj_error_message.value = "Please select a color"
                obj_error_message.visible = True
                page.update()
                return False
            return True
        
        def validate_inputs_for_Cylinder():
            if validate_inputs_for_sphere() == False:
                return False
            elif cylinder_radius.visible == False:
                obj_error_message.value = "Please enter a radius"
                obj_error_message.visible = True
                page.update()
                return False
            elif cylinder_allignment.value == None:
                obj_error_message.value = "Please select an allignment"
                obj_error_message.visible = True
                page.update()
                return False
            elif colour_button.visible == True and selected_color == None:
                obj_error_message.value = "Please select a color"
                obj_error_message.visible = True
                page.update()
                return False
            return True
        
       

        
        def string_coords_to_Vector(value):
            position_parts = value.split(",")
            x, y, z = map(int, position_parts)
            return Vector(x, y, z)
        
        def get_colour(list):
            return colour(list[0],list[1],list[2])
        
        def build_custom_object(obj_data):
            
            if obj_data["texture"] == "checker_texture":
                texture_colour1 = get_colour(obj_data["texture"]["colour1"])
                texture_colour2 = get_colour(obj_data["texture"]["colour2"])
                texture = checker_texture(texture_colour1,texture_colour2)
            elif obj_data["texture"] == "gradient_texture":
                texture_colour1 = get_colour(obj_data["texture"]["colour1"])
                texture_colour2 = get_colour(obj_data["texture"]["colour2"])
                texture = gradient_texture(texture_colour1,texture_colour2)
            elif obj_data["texture"] == "noise_texture":
                texture_colour1 = get_colour(obj_data["texture"]["colour1"])
                texture_colour2 = get_colour(obj_data["texture"]["colour2"])
                texture = noise_texture(texture_colour1,texture_colour2)
            else:
                texture = None
            obj_material = [float(obj_data["material"][0]),float(obj_data["material"][1]),float(obj_data["material"][2]),float(obj_data["material"][3])] 
            obj_colour = get_colour(obj_data["colour"])
            if obj_data["type"] == "Floor":
                myobj1 = Floor(obj_colour,obj_material,texture)
            
            elif obj_data["type"] == "Sphere":
                position = Vector(obj_data["center"][0],obj_data["center"][1],obj_data["center"][2])
                radius = float(obj_data["radius"])
                myobj1 = Sphere(position, radius,obj_colour,obj_material,texture)
            elif obj_data["type"] == "Cone":
                tip = Vector(obj_data["tip"][0],obj_data["tip"][1],obj_data["tip"][2])
                axis = Vector(obj_data["cone_axis"][0],obj_data["cone_axis"][1],obj_data["cone_axis"][2])
                angle = float(obj_data["cone_angle"])
                height = float(obj_data["height"])
                myobj1 = Cone(tip,axis,angle,height,obj_colour,obj_material,texture)
            elif obj_data["type"] == "Ellipsoid":
                position = Vector(obj_data["center"][0],obj_data["center"][1],obj_data["center"][2])
                abc = Vector(obj_data["abc"][0],obj_data["abc"][1],obj_data["abc"][2])
                myobj1 = Ellipsoid(position, abc,obj_colour,obj_material,texture)
            elif obj_data["type"] == "Cylinder":
                position = Vector(obj_data["center"][0],obj_data["center"][1],obj_data["center"][2])
                radius = float(obj_data["cylinder_radius"])
                height = float(obj_data["height"])
                if obj_data["cylinder_allignment"] == "Horizontal(X)":
                    myobj1 = Cylinder(position,"x",height,radius,obj_colour,obj_material,texture)
                elif obj_data["cylinder_allignment"] == "Vertical(y)":
                    myobj1 = Cylinder(position,"y",height,radius,obj_colour,obj_material,texture)
                else:
                    myobj1 = Cylinder(position,"z",height,radius,obj_colour,obj_material,texture)
            
            return myobj1



        def add_object(e):   #adds an object to the scene
            
            if object_type.value == None:
                obj_error_message.value = "Please select an object type"
                obj_error_message.visible = True
                page.update()
            elif object_type.value == "Sphere" and validate_inputs_for_sphere() == False:
                pass
            elif object_type.value == "Floor" and validate_inputs_for_floor() == False:
                pass
            elif object_type.value == "Cone" and validate_inputs_for_cone() == False:
                pass
            elif object_type.value == "Ellipsoid" and validate_inputs_for_Ellipsoid() == False:
                pass
            elif object_type.value == "Cylinder" and validate_inputs_for_Cylinder() == False:
                pass
            
            else:
                if object_type.value.startswith("Custom"):
                    if ":" in object_type.value:
                        hyphen = object_type.value.find("-")
                        obj_id = int(object_type.value[7:hyphen])
                        myobj1 = build_custom_object(load_object(get_user_id(username.value),obj_id))
                    else:
                        myobj1 = saved_objects[int(object_type.value[6:])]
                else:
                    obj_error_message.visible = False
                    
                    if texture_type.value == "Checkerboard":
                        if texture_colour1 == None or texture_colour2 == None:
                            obj_error_message.value = "Please select both colours for the checkerboard"
                            obj_error_message.visible = True
                            page.update()
                            return
                        object_texture = checker_texture(colour.hex_to_rgb(texture_colour1),colour.hex_to_rgb(texture_colour2))
                    elif texture_type.value == "Gradient":
                        if texture_colour1 == None or texture_colour2 == None:
                            obj_error_message.value = "Please select both colours for the gradient"
                            obj_error_message.visible = True
                            page.update()
                            return
                        object_texture = gradient_texture(colour.hex_to_rgb(texture_colour1),colour.hex_to_rgb(texture_colour2))
                    elif texture_type.value == "Noise":
                        if texture_colour1 == None or texture_colour2 == None:
                            obj_error_message.value = "Please select both colours for the noise"
                            obj_error_message.visible = True
                            page.update()
                            return
                        object_texture = noise_texture(colour.hex_to_rgb(texture_colour1),colour.hex_to_rgb(texture_colour2))
                    else:
                        object_texture = None
                    
                    obj_material = [float(Diffuse_input.text_field.value),float(Specular_input.text_field.value),float(Ambient_input.text_field.value),float(reflectivity_input.text_field.value)] 

                    print(obj_material)
                    print(material_type.value)
                    if object_type.value == "Floor":
                        myobj1 = Floor(colour.hex_to_rgb(selected_color),obj_material,object_texture)
                    elif object_type.value == "Cone":
                        tip = string_coords_to_Vector(object_position.value)
                        axis = string_coords_to_Vector(cone_axis.value)
                        angle = float(math.radians(float(cone_angle.value)))
                        height = float(object_radius.value)
                        myobj1 = Cone(tip,axis,angle,height,colour.hex_to_rgb(selected_color),obj_material,object_texture)
                    elif object_type.value == "Ellipsoid":
                        position = string_coords_to_Vector(object_position.value)
                        a = float(object_abc.controls[0].value)
                        b = float(object_abc.controls[1].value)
                        c = float(object_abc.controls[2].value)
                        abc = Vector(a,b,c)
                        myobj1 = Ellipsoid(position, abc,colour.hex_to_rgb(selected_color),obj_material,object_texture)
                    elif object_type.value == "Cylinder":
                        position = string_coords_to_Vector(object_position.value)
                        radius = float(cylinder_radius.value)
                        height = float(object_radius.value)
                        if cylinder_allignment.value == "Horizontal(X)":
                            myobj1 = Cylinder(position,"x",height,radius,colour.hex_to_rgb(selected_color),obj_material,object_texture)
                        elif cylinder_allignment.value == "Vertical(y)":
                            myobj1 = Cylinder(position,"y",height,radius,colour.hex_to_rgb(selected_color),obj_material,object_texture)
                        else:
                            myobj1 = Cylinder(position,"z",height,radius,colour.hex_to_rgb(selected_color),obj_material,object_texture)
                    else:
                        position = string_coords_to_Vector(object_position.value)
                        myobj1 = globals()[object_type.value](position, float(object_radius.value),colour.hex_to_rgb(selected_color),obj_material,object_texture)
                
                scene_objects.append(myobj1)
            
                added_objects.controls.append(
                    ft.Row(
                        [(ft.Text(f"Type: {object_type.value} Position: {object_position.value}, Color: {selected_color}")),
                         Remove_ButtonLite(text="Remove", on_click=lambda e: remove_object(e, myobj1)),
                         Remove_ButtonLite(text="Save Object", on_click=lambda e: save_custom_object(e, myobj1)) ,] , 
                         alignment=ft.MainAxisAlignment.CENTER
                    ),
                
                )
                
                page.update()

        def remove_object(e, object):  #removes object from the scene
            onum = scene_objects.index(object)
            scene_objects.pop(onum)
            added_objects.controls.pop(onum)
            page.update()
        
        def save_custom_object(e,object):   #saves object to user
            if User_Status:
                global custom_object
                custom_object = object                
                page.open(custom_object_name_dlg)
                page.update()
            else:
                if len(saved_objects) > 0:
                    obj_num = saved_objects.index(object)
                    obj_name = "Custom" + str(obj_num)
                else:
                    obj_name = "Custom0"
                object_type.options.append(ft.dropdown.Option(obj_name,on_click= add_custom_ui)) # saved locally via list
                saved_objects.append(object)
                obj_error_message.value = "Object saved and can be accessed in object type"
                obj_error_message.visible = True
                page.update()
        
        def on_object_name_submit():
                object = custom_object
                object_name = custom_object_name.value
                save_object(get_user_id(username.value),object,object_name)
                
                if len(saved_objects) > 0:
                    obj_num = saved_objects.index(object)
                    obj_name = "Custom" + str(obj_num)
                else:
                    obj_name = "Custom0"
                
                object_type.options.append(ft.dropdown.Option(obj_name,on_click= add_custom_ui)) # saved locally via list
                saved_objects.append(object)
                obj_error_message.value = "Object saved and can be accessed in object type"
                obj_error_message.visible = True
                page.update()



        def update_dimensions(e):   #updates the dimensions of the scene dynamically 
            current_width.value = f"Current Width: {width_input.value}"
            current_height.value = f"Current Height: {height_input.value}"
            page.update()
        

        
        def minus_click(text_field,minimum,step):
            value = round(float(text_field.value) - step, 1)
            if value <= minimum:
                obj_error_message.value = f"Coefficients must be more than {minimum}"
                obj_error_message.visible = True
            else:
                obj_error_message.visible = False
                text_field.value = str(value)
            
            page.update()
        
        
        def plus_click(text_field,maximum,step):
            value = round(float(text_field.value) + step, 1)
            if value > maximum:
                obj_error_message.value = f"Coefficients must be less than {maximum}"
                obj_error_message.visible = True
            else:
                obj_error_message.visible = False
                text_field.value = str(value)
            
            page.update()

        global texture_colour1
        texture_colour1 = None
        global texture_colour2
        texture_colour2 = None
        
        def get_texture_colour1(colour):
            global texture_colour1
            texture_colour1 = colour
        def get_texture_colour2(colour):
            global texture_colour2
            texture_colour2 = colour

        
        
        def add_texture(texture):
            
            
            
            
            if texture == "Checkerboard" or texture == "Gradient" or texture == "Noise":
                
                
                
                if double_colour_texture_buttons.visible:
                    colour_button.visible = True
                    texture_type.value = None
                    double_colour_texture_buttons.visible = False
                
                else:
                    colour_button.visible = False
                    double_colour_texture_buttons.visible = True
   
                
            page.update()
                
                

        
        def add_material(material,colour_check): 
            material_tile.visible = False
            
            material_colour = {

            }
            
            material_coeffs = {
                "Plastic": [0.6,0.2,0.2,0.0],
                "Matte" : [0.8,0.1,0.1,0.0],
                "Glossy" : [0.8,0.5,0.1,0.3],
                

                }
            
            print(f"the material is {material}")
            Diffuse_input.text_field.value = str(material_coeffs[material][0])
            Specular_input.text_field.value = str(material_coeffs[material][1])
            Ambient_input.text_field.value = str(material_coeffs[material][2])
            reflectivity_input.text_field.value = str(material_coeffs[material][3])
            
            if colour_check:
                colour_button.visible = False
                global selected_color
                selected_color = material_colour[material]
            
            
            page.update()


        def add_material_tile(e):
            material_tile.visible = True
            page.update()
        
  
        class IntField(ft.Container):
            def __init__(self,name,min,max,default="0.0",step=0.1):
                super().__init__()
                self.text_field = ft.TextField(
                    label=str(name),
                    value=default,
                    text_align=ft.TextAlign.RIGHT,
                    width=90
                )
                self.content = ft.Row(
                    [
                        ft.IconButton(
                            icon=ft.icons.REMOVE, 
                            on_click=lambda e: minus_click(self.text_field,min,step),
                            icon_size=20,
                            padding= 1
                        ),
                        self.text_field,
                        ft.IconButton(
                            icon=ft.icons.ADD, 
                            on_click=lambda e: plus_click(self.text_field,max,step),
                            icon_size= 20,
                            padding= 1
                        ),
                    ]
                )
        
        
        
        
        def convert_ppm_to_png(ppm_path, png_path):
            with open(ppm_path, "rb") as f:
                header = f.readline().strip()  # Read the magic number (P6 or P3)
                dimensions = f.readline().strip()  # Read the width and height
                maxval = int(f.readline().strip())  # Read the maximum color value

                # Parse dimensions
                width, height = map(int, dimensions.split())

                if header == b"P6":
                    # Binary PPM
                    dtype = "uint8" if maxval <= 255 else "uint16"
                    image_data = np.fromfile(f, dtype=dtype)

                    if maxval > 255:
                        image_data = (image_data / maxval * 255).astype("uint8")

                    # Reshape the binary data
                    image_data = image_data.reshape((height, width, 3))

                elif header == b"P3":
                    # ASCII PPM
                    data = f.read().decode("ascii").split()
                    image_data = np.array(data, dtype=int).reshape((height, width, 3))

                    if maxval > 255:
                        image_data = (image_data / maxval * 255).astype("uint8")

                else:
                    # Unsupported format
                    raise ValueError("Unsupported PPM format. Only P3 (ASCII) and P6 (binary) are supported.")

            # Convert the data to a PIL Image and save as PNG
            image = Image.fromarray(image_data.astype("uint8"), mode="RGB")
            image.save(png_path, "PNG")
        
        def final_validation():   #validates the scene before rendering
            
            
            if lights == []:
                light_error_message.value = "Please enter a light source"
                light_error_message.visible = True
                page.update()
                return False
            elif ("scene_camera" in globals()) == False:
                light_error_message.visible = False
                
                cam_error_message.value = "Please enter a camera position"
                cam_error_message.visible = True
                page.update()
                return False
            elif validlength(width_input.value) == False or validlength(height_input.value) == False:
                cam_error_message.visible = False
                
                scene_error_message.value = "Please enter valid dimensions of the scene "
                scene_error_message.visible = True
                page.update()
                return False
            elif scene_objects == []:
                scene_error_message.visible = False

                obj_error_message.value = "Please enter an object"
                obj_error_message.visible = True
                page.update()
                return False
            
            else:
                return True
        
        
        def render(e):   #renders the scene
            print(f"the top control is {page.controls[0]} ")
            
            if img.src:
                page.controls.pop(0)
                img.src = None
            
            img.src = None

            page.update()

            global scene_name
            print(f"the scene name is {scene_name}")
            
            if scene_name == None:
                scene_name = "image"

            timestamp = datetime.today().strftime('%Y-%m-%d_%H_%M_%S')

            scene_name_png = scene_name + timestamp + ".png"
            scene_name_ppm = scene_name + timestamp +".ppm"
            
            current_name.value = f"Current Name: {scene_name}"

            if final_validation() == False:
                pass
            else:
                scene_error_message.visible = False
                pb.visible = True
                pb.value = 0
                
                scene_width = int(width_input.value)
                scene_height = int(height_input.value)
                user_scene = Scene(scene_objects,scene_camera,scene_width,scene_height,lights)  
                
                Engine = engine()
                image = Engine.render(user_scene)
                
                with open(scene_name_ppm, "w") as img_file:
                    image.write_ppm(img_file)

                convert_ppm_to_png(scene_name_ppm, scene_name_png)
                
                os.remove(scene_name_ppm)   #deletes the ppm file after conversion

                if User_Status:
                    os.rename(scene_name_png, f"User_Data/{get_user_id(username.value)}/{scene_name_png}")
                    img.src = f"User_Data/{get_user_id(username.value)}/{scene_name_png}"
                else:
                    img.src = scene_name_png
        

                page.update()
                
                print("######################")
                for i in range(0, 101):    #loading a progress bar not accurate of the rendering speed but for decoration
                    pb.value = i * 0.02
                    sleep(0.01)
                    page.update()
                  
                img_viewer.content = img
                page.controls.insert(0, img_tile)
                img.visible = True
                page.update()

                pb.visible = False
                pb.value = 0
                page.update()


                
        
        def test_render(e):   #renders a test image
            if img.src:
                page.controls.pop(0)
                img.src = None
            
            
            page.update()
            
            Engine = engine()
            test_objs = [Sphere(Vector(0, 0, 5), 0.5, colour(1, 0, 0))]
            test_cam = camera(Vector(0, 0, -1))
            test_lights = [light(Vector(0, 0, 0), colour(1, 1, 1))]
            test_scene = Scene(test_objs, test_cam, 300, 200, test_lights)
            test_image = Engine.render(test_scene)
            with open("test_image.ppm", "w") as img_file:
                test_image.write_ppm(img_file)
            convert_ppm_to_png("test_image.ppm", "test_image.png")
            
            os.remove("test_image.ppm")   #deletes the ppm file after conversion

            img.src = "test_image.png"
            pb.visible = True
            pb.value = 0
            
            for i in range(0, 101):    #loading a progress bar not accurate of the rendering speed but for decoration
                pb.value = i * 0.02
                sleep(0.01) 
                page.update()
            
            
            img_viewer.content = img
            page.controls.insert(0, img_tile)
            pb.visible = False
            img.visible = True
            
            pb.value = 0

            page.update()

        
        def testy(e):
            render_name.value = "Testy"
            light_pos.value = "0,0,0"
            cam_pos.value = "0,0,-1"
            width_input.value = "300"
            height_input.value = "200"
            object_position.value = "0,0,5"
            object_radius.value = "0.5"
            page.update()

                
        
        
        def validate_name(value):   #validates the name of the render
            if re.fullmatch(r'[A-Za-z0-9#_]+', value):
                return True
            return False
        
        def set_name(e):   #sets the name of the render
            if validate_name(render_name.value):
                name_error_message.visible = False

                global scene_name
                scene_name = render_name.value
                current_name.value = f"Current Name: {scene_name}"
                
                page.update()
            else:
                name_error_message.value = "Please enter a name for the render"
                name_error_message.visible = True
                page.update()
            
        def sign_out(e):
            global User_Status
            User_Status = None
            page.controls.clear()
            username.value = ""
            password.value = ""
            loginpage()
            page.update()
        
        
        

        def load_custom_objects_to_ui():
            if User_Status:
                custom_objects = load_objects(get_user_id(username.value))
                for obj in custom_objects:
                    object_type.options.append(ft.dropdown.Option(f"Custom:{obj[0]}-{obj[1]}",on_click= add_custom_ui))
                page.update()
                        
        img_carousel = ft.Row(expand=1, wrap=False, scroll="always")
        
        def edit(src):
            img.src = src
            img_viewer.content = img
            img.visible = True
            img_showcaser(e)
        
        def my_renders(e):
            page.controls.clear()
            
            scenes = get_scenes(get_user_id(username.value))
            image_paths = [row[0] for row in scenes]
            for image_path in image_paths:
                
                
                add = ft.Column(
                    [ft.Image(src=image_path,width=300,height=200,fit=ft.ImageFit.CONTAIN,),
                     ft.Text(image_path.split("/")[-1]),
                     ft.IconButton(icon=ft.icons.EDIT_SQUARE, on_click=lambda e,source=image_paths[image_paths.index(image_path)] :edit(source)),],
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,)
                img_carousel.controls.append(add)
                page.update()
            
            page.add(
                theme_switch_button,
                ft.Column( 
                    [
                        ft.Text("My Renders", size=30, weight=ft.FontWeight.BOLD),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,  
                ),
                img_carousel,
                main_menu_Button,
                Sign_out_Button,
                

            )
            page.update()
        
        global selected_color
        selected_color = None  # Holds the selected colorrender
        
        
        def add_custom_ui(e):
            remove_ui()
            page.update()
        
        def add_floor_ui(e):
            remove_ui()
            page.update()
        
        
        def add_Sphere_ui(e):
            remove_ui()
            object_position.visible = True
            object_radius.visible = True
            object_position.label = "Object Position"
            object_radius.label = "Object Radius"
            page.update()

        def add_cone_ui(e):
            remove_ui()
            object_position.visible = True
            object_radius.visible = True
            object_position.label = "Cone Tip/corner Position"
            object_radius.label = "Cone Height"
            cone_angle.visible = True
            cone_axis.visible = True
            page.update()


        def add_Ellipsoid_ui(e):
            remove_ui()
            object_position.visible = True
            object_position.label = "Object Position"
            object_abc.visible = True
            page.update()
            
        def add_Cylinder_ui(e):
            remove_ui()
            object_position.visible = True
            object_position.label = "Object Position"
            cylinder_allignment.visible = True
            cylinder_radius.visible = True
            cylinder_radius.label = "Cylinder Radius"
            object_radius.visible = True
            object_radius.label = "Cylinder Height"
            page.update()

        def remove_ui():
            for x in object_tile.controls:
                if x._get_control_name() == "text":
                    if x.value == "Stopper":
                        print("stopped")
                        break
                    else:
                        x.visible = False
                elif x._get_control_name() == "dropdown":
                    if x.label == "Object Type":
                        pass
                    else:
                        x.visible = False
                else:
                    x.visible = False

        def close_custom_object_dlg(e):
            page.close(custom_object_name_dlg)
            page.update()
            on_object_name_submit()
        
        custom_object_name = ft.TextField(label="Object Name",hint_text="e.g., MyFavouriteSphere", width=600,border_color=ft.colors.GREEN_800)
        custom_object_name_dlg = ft.AlertDialog(
            modal=True,
            title=ft.Text("Please confirm a name for custom object"),
            content=custom_object_name,
            actions=[
                ft.TextButton("Ok", on_click=close_custom_object_dlg),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )

    
        

        render_name = ft.TextField(label="Render Name",hint_text="e.g., My_Render", width=600,border_color=ft.colors.GREEN_800)
        light_pos = ft.TextField(label="Light Source Postion",hint_text="e.g. x, y, z", width=600,border_color=ft.colors.GREEN_800)
        cam_pos = ft.TextField(label= "Camera Postion",hint_text="e.g. x, y, z", width=600,border_color=ft.colors.GREEN_800)
        width_input = ft.TextField(label = "Width",hint_text="e.g., 300", width=200, on_change=update_dimensions,border_color=ft.colors.GREEN_800)
        height_input = ft.TextField(label = "height",hint_text="e.g., 200", width=200, on_change=update_dimensions,border_color=ft.colors.GREEN_800)

        current_width = ft.Text("Current Width: ")
        current_height = ft.Text("Current Height: ")
        current_name = ft.Text("Current Name: ")

        object_type = ft.Dropdown(
            label="Object Type",
            options=[ft.dropdown.Option("Sphere",on_click= add_Sphere_ui),
                     ft.dropdown.Option("Floor",on_click= add_floor_ui),
                     ft.dropdown.Option("Cone",on_click= add_cone_ui),
                     ft.dropdown.Option("Ellipsoid",on_click= add_Ellipsoid_ui),
                     ft.dropdown.Option("Cylinder",on_click= add_Cylinder_ui),
                     ],
            width=150,
            border_color= ft.colors.GREEN_800,
        )

        load_custom_objects_to_ui()
   
        
        pb = ft.ProgressBar(width=400)
        pb.visible = False
        set = MyButton(text="Set", on_click=set_name)
        object_position = ft.TextField(label="Object Position", hint_text="e.g., (x, y, z)", width=150,border_color=ft.colors.GREEN_800)
        object_radius = ft.TextField(label="Object Radius", hint_text="e.g., 0.5", width=150,border_color=ft.colors.GREEN_800)

        cone_axis = ft.TextField(label="Cone Axis", hint_text="e.g., (x, y, z)", width=150,border_color=ft.colors.GREEN_800)
        cone_angle = ft.TextField(label="Cone Angle", hint_text="e.g., 45", width=150,border_color=ft.colors.GREEN_800)
        cone_axis.visible = False
        cone_angle.visible = False



        object_abc = ft.Row(
            [
            IntField("X radius",0,100,1,1),
            IntField("Y radius",0,100,1,1),
            IntField("X radius",0,100,1,1),]
        )
        object_abc.visible = False

        cylinder_allignment = ft.Dropdown(
            label="Cylinder Allignment",
            options=[ft.dropdown.Option("Horizontal(X)"),
                     ft.dropdown.Option("Vertical(y)"),
                     ft.dropdown.Option("Depth(z)"),
                     ],
            width=150,
            border_color= ft.colors.GREEN_800,
        )
        cylinder_radius = ft.TextField(label="Cylinder Radius", hint_text="e.g., 0.5", width=150,border_color=ft.colors.GREEN_800)
        #cylinder height is object radius
        cylinder_radius.visible = False
        cylinder_allignment.visible = False

        Ambient_input = IntField("Ambient",0,1)
        Diffuse_input = IntField("Diffuse",0,1,0.5)
        Specular_input = IntField("Specular",0,1,0.5)
        reflectivity_input = IntField("Reflectivity",0,1)
        
        
        material_type = ft.Dropdown(
            label= "Material Type",
            options=[(ft.dropdown.Option("Plastic",on_click= lambda e: add_material("Plastic",False) ) ) , 
                    (ft.dropdown.Option("Matte",on_click= lambda e: add_material("Matte",False) ) ),
                    (ft.dropdown.Option("Glossy",on_click= lambda e: add_material("Glossy",False) ) ),
                     
                    (ft.dropdown.Option("Custom", on_click= add_material_tile))],
            width=150,
            border_color= ft.colors.GREEN_800,

        )
        
        texture_type = ft.Dropdown(
            label= "Texture Type",
            options=[(ft.dropdown.Option("Checkerboard",on_click= lambda e: add_texture("Checkerboard") ) ) ,
                     (ft.dropdown.Option("Gradient",on_click= lambda e: add_texture("Gradient") ) ) , 
                     (ft.dropdown.Option("Noise",on_click= lambda e: add_texture("Noise") ) ) ,  
                    
                     
                    ],
            width=150,
            border_color= ft.colors.GREEN_800,
        )
        

        
        material_tile = ft.Row(
            [Diffuse_input,Specular_input,Ambient_input,reflectivity_input],

        )
        material_tile.visible = False
        
        
        
        add_cam_button = MyButton(text="Add Camera", on_click=add_cam)
        add_object_button = MyButton(text="Add Object", on_click=add_object)
        add_light_button = MyButton(text="Add Light", on_click=add_light)
        
        
        
        light_error_message = ft.Text(
        "",
        color= ft.colors.RED,
        visible=False,
        )
        cam_error_message = ft.Text(
        "",
        color= ft.colors.RED,
        visible=False,
        )
        obj_error_message = ft.Text(
        "",
        color= ft.colors.RED,
        visible=False,
        )
        scene_error_message = ft.Text(
        "",
        color= ft.colors.RED,
        visible=False,
        )
        name_error_message = ft.Text(
        "",
        color= ft.colors.RED,
        visible=False,
        )

        def put_in_selected(colour):
            global selected_color
            selected_color = colour
            print(selected_color)
        
        def pick_color(func):
            def open_color_picker(e):
                # Add the dialog to the page overlay
                if d not in e.control.page.overlay:
                    e.control.page.overlay.append(d)
                d.open = True
                e.control.page.update()

            color_picker = ColorPicker(color="#c8df6f", width=300)
            color_icon = ft.IconButton(icon=ft.icons.BRUSH, on_click=open_color_picker)

            def change_color(e):
                color_icon.icon_color = color_picker.color
                # global selected_color
                # selected_color = color_picker.color
                if func:
                    func(color_picker.color)
                
                d.open = False
                e.control.page.update()

            def close_dialog(e):
                d.open = False
                e.control.page.update()

            d = ft.AlertDialog(
                content=color_picker,
                actions=[
                    ft.TextButton("OK", on_click=change_color),
                    ft.TextButton("Cancel", on_click=close_dialog),
                ],
                actions_alignment=ft.MainAxisAlignment.END,
                on_dismiss=change_color,
            )

            return color_icon
        
        

        double_colour_texture_buttons = ft.Row(
            [
            ft.Text(f"Colour 1"),
            pick_color(get_texture_colour1),
            
            ft.Text(f"Colour 2"),
            pick_color(get_texture_colour2),
                    
            ]
        )
        
        double_colour_texture_buttons.visible = False
        colour_button = pick_color(put_in_selected)
        
        Sign_out_Button= Fancy_Button(text="Sign Out", on_click=sign_out,)
        My_Renders_Button= Fancy_Button(text="My Renders", on_click=my_renders,)
        main_menu_Button= Fancy_Button(text="Main Menu", on_click=switch_to_main_ui,)
        
        if User_Status == True:
            My_Renders_Button.visible = True
        else:
            My_Renders_Button.visible = False
        
        def remove_img_from_library(img_path):
            userID = get_user_id(username.value)
            remove_scene(userID,img_path)

        
        
        def remove_img(e):
            if img.src == "test_image.png":
                pass
            else:
                if scene_name in names:
                    names.remove(scene_name)
                if User_Status:
                    remove_img_from_library(img.src)
                    
            os.remove(img.src)            
            img.src = None
            page.controls.pop(0)
            page.update()
            if page_tracker != "main":
                main_menu_Button.on_click(e)
        
        
        def img_to_library(e):
            
            
            
            userID = get_user_id(username.value)
            
            create_scene(userID,img.src,scene_name)

            page.add(ft.Text(f"{scene_name} added to library"))
            page.update()
            

        

        def download_file(file_path):
    
            def directory_picker_result(e: FilePickerResultEvent):
                if e.path:
                    shutil.copy(file_path, e.path)
                    print(f"Selected directory: {e.path}")
                else:
                    print("No directory selected")
                
                page.update()
                        
            file_picker = FilePicker(on_result=directory_picker_result)
            page.add(file_picker)
            file_picker.get_directory_path(dialog_title="Select Directory")

            page.overlay.append(file_picker)

            file_picker.get_directory_path(dialog_title="Select Directory")
            page.update()

       


        def copy_image_to_clipboard(image_path):
            try:                
                image = Image.open(image_path)
                
                output = io.BytesIO()
                image.convert("RGB").save(output, "BMP")
                bmp_data = output.getvalue()[14:]  
                output.close()

                win32clipboard.OpenClipboard()
                win32clipboard.EmptyClipboard()
                win32clipboard.SetClipboardData(win32clipboard.CF_DIB, bmp_data)
                win32clipboard.CloseClipboard()

                print("Image successfully copied to the clipboard!")

            except Exception as e:
                print(f"Error copying image to clipboard: {e}")
        
        def img_showcaser(e):
            page.controls.clear()
            page_tracker = "showcaser"
            print("the image is ",img.src)
            if User_Status:
                page.add(
                    theme_switch_button,
                    img_viewer,
                    ft.Row([
                        ft.IconButton(icon=ft.icons.ADD ,tooltip= "add to library", on_click=img_to_library),
                        ft.IconButton(icon=ft.icons.DOWNLOAD ,tooltip= "download", on_click=lambda e: download_file(img.src)),
                        ft.IconButton(icon=ft.icons.DELETE ,tooltip= "delete", on_click=remove_img),
                        ft.IconButton(icon=ft.icons.CONTENT_COPY ,tooltip= "Copy", on_click= lambda e: copy_image_to_clipboard(img.src)),],    
                    alignment=ft.MainAxisAlignment.CENTER,
                    ),
                    
                    main_menu_Button,
                    Sign_out_Button,
                    

                )
                page.update()
            else:
                page.add(
                    theme_switch_button,
                    img_viewer,
                    ft.Row([
                        ft.IconButton(icon=ft.icons.DOWNLOAD ,tooltip= "download", on_click=lambda e: download_file(img.src)),
                        ft.IconButton(icon=ft.icons.CONTENT_COPY ,tooltip= "Copy", on_click= lambda e: copy_image_to_clipboard(img.src)),
                        ft.IconButton(icon=ft.icons.DELETE ,tooltip= "delete", on_click=remove_img),],    
                    alignment=ft.MainAxisAlignment.CENTER,
                    ),
                    Sign_out_Button,
                )
                page.update()
            
        
        
        img_viewer = ft.InteractiveViewer(
            min_scale=0.1,
            max_scale=15,
            boundary_margin=ft.margin.all(20),
            content=img,
        )

        img_tile = ft.Row(
            [img_viewer, 
            
            ft.Column(
            [ft.IconButton(icon=ft.icons.CHECK , on_click=img_showcaser),
            ft.IconButton(icon=ft.icons.DELETE, on_click=remove_img),
            ],
            )
            
            
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        )
        
        stopper = ft.Text("Stopper")
        stopper.visible = False
        
        object_tile = ft.Row(
            [
                object_type,
                object_position,
                object_abc,
                cylinder_allignment,
                cone_axis,
                cone_angle,
                object_radius,  #sometimes height
                cylinder_radius,
                stopper,
                material_tile,
                material_type,
                ft.Column([texture_type,double_colour_texture_buttons]),
                colour_button,
                add_object_button,
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=10,
        )
   
      


        page.add(
            
            pb,
            theme_switch_button,
            ft.Column(
                [
                    ft.Row(
                        [render_name,set], alignment=ft.MainAxisAlignment.CENTER
                        
                    ),
                    name_error_message,
                    current_name,
                    ft.Row(
                        [light_pos,add_light_button], alignment=ft.MainAxisAlignment.CENTER
                        
                    ),
                    light_error_message,
                    ft.Text("Added Lights:"),
                    added_lights,
                    
                    ft.Row(
                        [cam_pos,add_cam_button], alignment=ft.MainAxisAlignment.CENTER
                    ),
                    cam_error_message,
                    ft.Text("Added Cameras:"),
                    added_cam,
                    ft.Row([width_input, height_input], alignment=ft.MainAxisAlignment.CENTER),
                    ft.Row([current_width, current_height], alignment=ft.MainAxisAlignment.CENTER),
                    ft.Text("Objects", size=16, weight=ft.FontWeight.BOLD),
                    object_tile,
                    obj_error_message,
                    ft.Text("Added Objects:"),
                    added_objects,  # Display added objects
                    ft.Row([R_Button(text="Render", on_click=render)], alignment=ft.MainAxisAlignment.CENTER),
                    scene_error_message,
                    ft.Row([Sign_out_Button,R_Button(text="Test Render", on_click=test_render),My_Renders_Button], alignment=ft.MainAxisAlignment.CENTER),
                    ft.Row([R_Button(text="Testy", on_click=testy)], alignment=ft.MainAxisAlignment.CENTER),
                    
                
                ],
                alignment=ft.MainAxisAlignment.CENTER,  # Center vertically
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,  # Center horizontally
                scroll=ft.ScrollMode.ALWAYS,
                expand=True,  # Add this to allow the column to expand
                height=page.height,  # Add this to make the column take full height
                spacing=10,
            )
        )
        
        page.scroll = ft.ScrollMode.ALWAYS
        page.update()
        
        
        

    # Initial login UI
    username = ft.TextField(label="Username", width=300,border_color=ft.colors.GREEN_800)
    password = ft.TextField(label="Password", password=True, width=300,border_color=ft.colors.GREEN_800)
    
    error_message = ft.Text(
        "",
        color= ft.colors.RED,
        visible=False,  
    )
    
    login_button = ft.ElevatedButton(text="Login", on_click=login)
    register_button = ft.ElevatedButton(text="Register", on_click=register)
    guest_button = ft.ElevatedButton(text="Continue as Guest", on_click=guest)
    
    def loginpage():
        
        global names 
        names = []

        page.vertical_alignment = ft.MainAxisAlignment.CENTER
        page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    
        page.add(
            theme_switch_button,

            ft.Column(
                [
                    ft.Text("Welcome to RayTray", size=20, weight=ft.FontWeight.BOLD),
                    username,
                    password,
                    ft.Row(
                        [
                            login_button,
                            register_button,

                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        spacing=10,
                    ),
                    error_message,
                    guest_button,

                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            )
        )



        page.update()

    loginpage()

ft.app(main)

