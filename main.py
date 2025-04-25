#My libraries
from image import colour
from Maths import Vector
from objects import *
from engine import engine
from scene import Scene,camera
from light import light
from loginsys import create_user,login_user,get_user_id
from scenes_table import create_scene,get_scenes,remove_scene,get_scene_data,get_scene_data_from_db
from object_table import save_object,load_objects,load_object,get_obj_id
from textures import *

#3rd part libraries
import flet as ft
from flet_contrib.color_picker import ColorPicker
from flet import FilePicker, FilePickerResultEvent
from PIL import Image
import numpy as np
import re
import time
import os
import shutil
import win32clipboard
import io
from datetime import datetime
import copy
import threading


saved_scene_data = None

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
    
    
    def username_sanitate(value:str) -> bool:
        if re.fullmatch(r'[A-Za-z0-9#_]+', value):
            return True
        return False   #checks if the username is valid
    
    
    def password_sanitate(value:str) -> bool: 
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
        
        if not (create_user(usern,pwd)):
            error_message.value = "Username already exists"
            error_message.visible = True
            page.update()
            return
        
        path = f'C:/Users/jobyk/python/RayTrayNEA/User_Data/{get_user_id(usern)}' 
        if not os.path.exists(path):
            print("Made user folder")
            os.makedirs(path)
        
        
        global User_Status
        User_Status = True

     

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
        

        
        
        switch_to_main_ui(e)   #switches to the main UI when the user logs in successfully
    
    
    def switch_to_main_ui(e):
        global page_tracker
        page_tracker = "main"
        
        error_message.visible = False
        
        global names

        
        
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

       
        def validcoord(value:str) -> bool:
            if re.fullmatch(r'-?\d+(\.\d+)?,-?\d+(\.\d+)?,-?\d+(\.\d+)?', value):
                return True
            return False
        
        def validradius(value:str) -> bool:
            if re.fullmatch(r'\d+(\.\d+)?', value):
                return True
            return False
        
        def validlength(value:str) -> bool:
            value = str(value)

            if re.fullmatch(r'\d+(\.\d+)?', value):
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
        
        
       
        
        
        
        
        

        
        
        

    
        def check_if_cam_light_overlap():
            if cam_pos.value != None and light_pos.value != None and cam_pos.value == light_pos.value :
                cam_error_message.value = "Camera and Light cannot be in the same position"
                cam_error_message.visible = True
                page.update()
                return False
            return True
        
        def add_light(e):    # adds a light source to the scene 
            
            
            if not(check_if_cam_light_overlap()):
                return
            
            if validcoord(light_pos.value):
                light_error_message.visible = False
                position_parts = light_pos.value.split(",")
                x, y, z = map(float, position_parts)
                if float(brightness_slider.value) <= 0.5:
                    light_error_message.value = "Warning: Brightness under 0.5 is too dim ,objects may not be clearly visible"
                    light_error_message.visible = True
                    
                
                mylight = light(Vector(x, y, z),colour(1,1,1),float(brightness_slider.value))
                lights.append(mylight)

                added_lights.controls.append(
                    ft.Row(
                        [(ft.Text(f"Position: {light_pos.value} Brightness: {brightness_slider.value}")),Remove_ButtonLite(text="Remove", on_click=lambda e: remove_light(e, mylight))] , alignment=ft.MainAxisAlignment.CENTER
                        
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
            
            if not(check_if_cam_light_overlap()):
                return

            if validcoord(cam_pos.value):
                if added_cam.controls != []:
                    cam_error_message.value = "Only one camera is allowed"
                    cam_error_message.visible = True
                    page.update()
                    return
                cam_error_message.visible = False
                cam_parts = cam_pos.value.split(",")
                x, y, z = map(float, cam_parts)
                global scene_camera
                scene_camera = camera(Vector(x, y, z),int(fov_slider.value))
                added_cam.controls.append(
                    ft.Row(
                        [(ft.Text(f"Position: {cam_pos.value} FOV: {fov_slider.value}")),Remove_ButtonLite(text="Remove", on_click=lambda e: remove_cam(e, scene_camera))] , alignment=ft.MainAxisAlignment.CENTER
                        
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
        
        
        def validate_inputs_for_Sphere():
            if validcoord(object_position.value) == False:
                obj_error_message.value = "Please enter a valid position"
                obj_error_message.visible = True
                page.update()
                return False
        
            elif validradius(object_radius.value) == False:
                obj_error_message.value = "Please enter a valid size"
                obj_error_message.visible = True
                page.update()
                return False
            elif colour_button.visible == True and selected_color == None:
                obj_error_message.value = "Please select a color"
                obj_error_message.visible = True
                page.update()
                return False
            return True
        
        def validate_inputs_for_Floor():

            if colour_button.visible == True and selected_color == None:
                obj_error_message.value = "Please select a color"
                obj_error_message.visible = True
                page.update()
                return False
            return True
        
        def validate_inputs_for_Cone():
            if validate_inputs_for_Sphere() == False:
                return False
            elif validcoord(cone_axis.value) == False:
                obj_error_message.value = "Please enter a valid axis"
                obj_error_message.visible = True
                page.update()
                return False
            elif cone_angle.value == None or cone_angle.value == "":
                obj_error_message.value = "Please enter a valid angle"
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
           
            return True
        
        def validate_inputs_for_Cylinder():
            if validate_inputs_for_Sphere() == False:
                return False
            elif cylinder_radius.visible == False or validradius(cylinder_radius.value) == False:
                obj_error_message.value = "Please enter a valid cylinder radius"
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
        
        def validate_inputs_for_Cube():
            if validate_inputs_for_Sphere() == False:
                return False
            
            if object_rotation.value:
                if validcoord(object_rotation.value) == False:
                    obj_error_message.value = "Please enter a valid Rotation Vector"
                    obj_error_message.visible = True
                    page.update()
                    return False
            return True
        
        def validate_inputs_for_Capsule():
            if validate_inputs_for_Cylinder() == False:
                return False
            return True

        def validate_inputs_for_Tetrahedron():
            if validate_inputs_for_Sphere() == False:
                return False
            return True
        
        def validate_inputs_for_Array():
            if validlength(number.text_field.value) == False:
                obj_error_message.value = "Please enter a valid number of objects"
                obj_error_message.visible = True
                page.update()
                return False
            return True

        
        def string_coords_to_Vector(value:str) -> object:
            position_parts = value.split(",")
            x, y, z = map(float, position_parts)
            return Vector(x, y, z)
        
        def get_colour(list) -> object:
            try:
                return colour(list[0],list[1],list[2])
            except:
                return None
                
        
        def list_to_to_Vector(list):
            return Vector(list[0],list[1],list[2])
        
        
        def update_dimensions(e):   #updates the dimensions of the scene dynamically 
            current_width.value = f"Current Width: {width_input.value}"
            current_height.value = f"Current Height: {height_input.value}"
            page.update()
        
        
        width_input = ft.TextField(label = "Width",hint_text="e.g., 300", width=200, on_change=update_dimensions,border_color=ft.colors.GREEN_800)
        height_input = ft.TextField(label = "height",hint_text="e.g., 200", width=200, on_change=update_dimensions,border_color=ft.colors.GREEN_800)
        
    
        def build_scene(scene_data):
            print("Building scene")
            width_input.value = int(scene_data["width"])

            height_input.value = int(scene_data["height"])


            for obj in scene_data["lights"]:
                
                lights.append( light( list_to_to_Vector(obj["position"]) ) )
                added_lights.controls.append(
                    ft.Row(
                        [(ft.Text(f"Position: {obj['position']} Brightness: {obj['brightness']}")),Remove_ButtonLite(text="Remove", on_click=lambda e: remove_light(e, lights[-1]))] , alignment=ft.MainAxisAlignment.CENTER
                        
                    ),
                )
            
            camera_position = scene_data["camera_position"]    
            camera_fov = scene_data["camera_fov"]    
            global scene_camera
            scene_camera = camera(list_to_to_Vector(camera_position),int(camera_fov))
            
            added_cam.controls.append(
                ft.Row(
                    [(ft.Text(f"Position: {camera_position} FOV: {camera_fov}")),Remove_ButtonLite(text="Remove", on_click=lambda e: remove_cam(e, scene_camera))] , alignment=ft.MainAxisAlignment.CENTER
                    
                ),
            )
            
            for obj in scene_data["objects"]:
                
                myobj1 = build_custom_object(obj)
                scene_objects.append(myobj1)
                add_to_added_objects(myobj1)
            
            page.update()

       
        
        def build_custom_object(obj_data:dict) -> object:
            
            if obj_data["texture"]:
                texture_colour1 = get_colour(obj_data["texture_colour1"])
                texture_colour2 = get_colour(obj_data["texture_colour2"])
                texture = globals()[obj_data["texture"]](texture_colour1,texture_colour2)
            else:
                texture = None
            
            obj_material = [float(obj_data["material"][0]),float(obj_data["material"][1]),float(obj_data["material"][2]),float(obj_data["material"][3])] 
            print(obj_data["colour"])
            obj_colour = get_colour(obj_data["colour"])
            
            if obj_data["type"] == "Floor":
                myobj1 = Floor(obj_colour,obj_material,texture)
            elif obj_data["type"] == "Sphere":
                position = list_to_to_Vector(obj_data["center"])
                radius = float(obj_data["radius"])
                myobj1 = Sphere(position, radius,obj_colour,obj_material,texture)
            elif obj_data["type"] == "Tetrahedron":
                position = list_to_to_Vector(obj_data["center"])
                side_length = float(obj_data["radius"])
                myobj1 = Tetrahedron(position,side_length,obj_colour,obj_material,texture)
            elif obj_data["type"] == "Cone":
    
                tip = list_to_to_Vector(obj_data["tip"])
                axis = list_to_to_Vector(obj_data["axis"])
                angle = float(obj_data["angle"])
                height = float(obj_data["height"])
                myobj1 = Cone(tip,axis,angle,height,obj_colour,obj_material,texture)
            elif obj_data["type"] == "Ellipsoid":
                position = list_to_to_Vector(obj_data["center"])
                abc = list_to_to_Vector(obj_data["abc"])
                myobj1 = Ellipsoid(position, abc,obj_colour,obj_material,texture)
            elif obj_data["type"] == "Cylinder":
                position = list_to_to_Vector(obj_data["center"])
                radius = float(obj_data["radius"])
                height = float(obj_data["height"])
                allignment = obj_data["allignment"]
                myobj1 = Cylinder(position,allignment,height,radius,obj_colour,obj_material,texture)
                
            elif obj_data["type"] == "Capsule":
                position = list_to_to_Vector(obj_data["center"])
                radius = float(obj_data["radius"])
                height = float(obj_data["height"])
                allignment = obj_data["allignment"]
                myobj1 = Capsule(position,allignment,height,radius,obj_colour,obj_material,texture)
                
 
            elif obj_data["type"] == "Cube":
                position = list_to_to_Vector(obj_data["center"])
                side_length = float(obj_data["radius"])
                object_rotation = list_to_to_Vector(obj_data["object_rotation"])
                myobj1 = Cube(position,side_length,object_rotation,obj_colour,obj_material,texture)
            
            return myobj1
        


        def validate_input_for_double_colour():
            if texture_colour1 == None and texture_colour2 != None:
                obj_error_message.value = "Please select BOTH colours for the texture"
                obj_error_message.visible = True
                page.update()
                return False
            elif texture_colour1 != None and texture_colour2 == None:
                obj_error_message.value = "Please select BOTH colours for the texture"
                obj_error_message.visible = True
                page.update()
                return False
            return True

        def validate_object():
            if object_type.value.startswith("Custom"):
                return True
            validation_functions = {
                "Sphere": validate_inputs_for_Sphere,
                "Cube": validate_inputs_for_Cube,
                "Cone": validate_inputs_for_Cone,
                "Ellipsoid": validate_inputs_for_Ellipsoid,
                "Cylinder": validate_inputs_for_Cylinder,
                "Capsule": validate_inputs_for_Capsule,
                "Floor": validate_inputs_for_Floor,
                "Tetrahedron": validate_inputs_for_Tetrahedron,
                "Array": validate_inputs_for_Array,

            }
            validator = validation_functions.get(object_type.value)
            if validator:
                return validator()
            else:
                print("object function not found")
                
        def handle_custom_object():
            if ":" in object_type.value:
                hyphen = object_type.value.find("-")
                obj_id = int(object_type.value[7:hyphen])
                myobj1 = build_custom_object(load_object(get_user_id(username.value),obj_id))
            else:
                myobj1 = saved_objects[int(object_type.value[6:])-1]
            
            return myobj1
        
        def handle_texture():
            if texture_type.value == "Image":
                if selected_image_texture_file_path.value == None:
                    obj_error_message.value = "Please select an image for the texture"
                    obj_error_message.visible = True
                    page.update()
                    object_texture = None
                else:
                    object_texture = image_texture(selected_image_texture_file_path.value)
            else:
                texture_class_name = texture_type.value.lower() + "_texture"
                texture_class = globals().get(texture_class_name)
                if texture_class == None:
                    raise ValueError(f"Texture class {texture_class_name} not found")

                if texture_colour1 != None and texture_colour2 != None:       #user chose optional colours
                    object_texture = globals()[texture_class_name](colour.hex_to_rgb(texture_colour1),colour.hex_to_rgb(texture_colour2))
                else:
                    print("user did not choose optional colours")
                    object_texture = globals()[texture_class_name]()     #user did not choose optional colours 
                       
            return object_texture
        
        def add_to_added_objects(myobj1):
            added_objects.controls.append(
                    ft.Row(
                        [(ft.Text(f"Type: {myobj1.__class__.__name__} , Texture: {myobj1.material.texture.__class__.__name__}")),
                         Remove_ButtonLite(text="Remove", on_click=lambda e: remove_object(e, myobj1)),
                         Remove_ButtonLite(text="Save Object", on_click=lambda e: save_custom_object(e, myobj1)) ,
                         ft.IconButton(icon=ft.icons.CONTENT_COPY_OUTLINED, icon_color=ft.colors.GREEN_800, on_click=lambda e: duplicate_object(e, myobj1))] , 
                         alignment=ft.MainAxisAlignment.CENTER
                    ),
                
                )


        if saved_scene_data != None:
            print("Loading scene data")
            build_scene(saved_scene_data)
            page.update()


        def add_object(e):   #adds an object to the scene
            
            if object_type.value == None:
                obj_error_message.value = "Please select an object type"
                obj_error_message.visible = True
                page.update()
            elif not(validate_object()):
                print("Invalid object")
                pass
            else:
                
                if object_type.value.startswith("Custom"):
                    myobj1 = handle_custom_object()
                else:
                    obj_error_message.visible = False
                    
                    if texture_type.value and texture_type.value != "None":
                        
                        if not(validate_input_for_double_colour()):
                            return
                        object_texture = handle_texture()
                        if object_texture == None:
                            return
                
                    else:
                        object_texture = None
                    
                    obj_material = [float(Diffuse_input.text_field.value),float(Specular_input.text_field.value),float(Ambient_input.text_field.value),float(reflectivity_input.text_field.value)] 

                    obj_colour = colour.hex_to_rgb(selected_color)
                    
                    #objects are then specifically handled due to the different parameters
                    if object_type.value == "Floor":
                        myobj1 = Floor(obj_colour,obj_material,object_texture)
                    
                    elif object_type.value == "Cone":
                        tip = string_coords_to_Vector(object_position.value)
                        axis = string_coords_to_Vector(cone_axis.value)
                        angle = float(math.radians(float(cone_angle.value)))
                        height = float(object_radius.value)
                        myobj1 = Cone(tip,axis,angle,height,obj_colour,obj_material,object_texture)
                    
                    elif object_type.value == "Ellipsoid":
                        position = string_coords_to_Vector(object_position.value)
                        a = float(object_abc.controls[0].text_field.value)
                        b = float(object_abc.controls[1].text_field.value)
                        c = float(object_abc.controls[2].text_field.value)
                        abc = Vector(a,b,c)
                        myobj1 = Ellipsoid(position, abc,obj_colour,obj_material,object_texture)
                    
                    elif object_type.value == "Cylinder":
                        position = string_coords_to_Vector(object_position.value)
                        radius = float(cylinder_radius.value)
                        height = float(object_radius.value)
                        if cylinder_allignment.value == "Horizontal(X)":
                            myobj1 = Cylinder(position,"x",height,radius,obj_colour,obj_material,object_texture)
                        elif cylinder_allignment.value == "Forward(y)":
                            myobj1 = Cylinder(position,"y",height,radius,obj_colour,obj_material,object_texture)
                        else:
                            myobj1 = Cylinder(position,"z",height,radius,obj_colour,obj_material,object_texture)
                    
                    elif object_type.value == "Capsule":
                        position = string_coords_to_Vector(object_position.value)
                        radius = float(cylinder_radius.value)
                        height = float(object_radius.value)
                        if cylinder_allignment.value == "Horizontal(X)":
                            myobj1 = Capsule(position,"x",height,radius,obj_colour,obj_material,object_texture)
                        elif cylinder_allignment.value == "Forward(y)":
                            myobj1 = Capsule(position,"y",height,radius,obj_colour,obj_material,object_texture)
                        else:
                            myobj1 = Capsule(position,"z",height,radius,obj_colour,obj_material,object_texture)
                    
                    elif object_type.value == "Cube":
                        position = string_coords_to_Vector(object_position.value)
                        side_length = float(object_radius.value)
                        if object_rotation.value == None or object_rotation.value == "":
                            rotation = Vector(0,0,0)
                        else:
                            rotation = string_coords_to_Vector(object_rotation.value)
                            rotation.x = float(math.radians(rotation.x))
                            rotation.y = float(math.radians(rotation.y))
                            rotation.z = float(math.radians(rotation.z))
                        myobj1 = Cube(position,side_length,rotation,obj_colour,obj_material,object_texture)
                    elif object_type.value == "Array":
                        
                        
                        build_array(int(float(number.text_field.value)))
                        added_objects.controls.append(ft.Text(f"Array of {number.text_field.value} objects added"))
                        page.update()
                        return
                        

                    else:   #sphere and tetrahedron
                        position = string_coords_to_Vector(object_position.value)      
                        myobj1 = globals()[object_type.value](position, float(object_radius.value),obj_colour,obj_material,object_texture)
                
                
                
                
                scene_objects.append(myobj1)
                add_to_added_objects(myobj1)
                
                    
                page.update()

        def remove_object(e, object):  #removes object from the scene
            onum = scene_objects.index(object)
            scene_objects.pop(onum)
            added_objects.controls.pop(onum)
            page.update()


        def build_array(obj_num):
            
            
            
            array_objects = []
            position = Vector(-30,5,21)
            
            initial = position.x
            for i in range(obj_num):
                if i > 0: 
                    position.x += 1
                if position.x == -initial:
                    position.z -= 1
                    position.x = initial
                obj_position = Vector(position.x, position.y, position.z)
                
                obj = Sphere(obj_position, 0.5,colour(1,0,0))
                array_objects.append(obj)

            
            
            scene_objects.extend(array_objects)
            
            

        def duplicate_object(e, object):  #duplicates object in the scene
            
            temp_object = copy.deepcopy(object)   #instead of temp_object = object
            
            scene_objects.append(temp_object)
            added_objects.controls.append(
                    ft.Row(
                        [(ft.Text(f"Type: {temp_object.__class__.__name__} , Color: {temp_object.colour.rgb_to_hex()}")),
                         Remove_ButtonLite(text="Remove", on_click=lambda e: remove_object(e, temp_object)),
                         Remove_ButtonLite(text="Save Object", on_click=lambda e: save_custom_object(e, temp_object)) ,
                         ft.IconButton(icon=ft.icons.CONTENT_COPY_OUTLINED, icon_color=ft.colors.GREEN_800, on_click=lambda e: duplicate_object(e, temp_object))] , 
                         alignment=ft.MainAxisAlignment.CENTER
                    ),
                )
            page.update()
                
        
        def save_custom_object(e,object):   #saves object to user
            if User_Status:
                global custom_object
                custom_object = object                
                page.open(custom_object_name_dlg)
                page.update()
            else:
                saved_objects.append(object)
                obj_name = "Custom" + str(len(saved_objects))
                object_type.options.append(ft.dropdown.Option(obj_name,on_click= add_custom_ui)) # saved locally via list
                obj_error_message.value = "Object saved and can be accessed in object type"
                obj_error_message.visible = True
                page.update()
        
        def on_object_name_submit():
                object = custom_object
                object_name = custom_object_name.value
                
                object_name += datetime.today().strftime('%Y-%m-%d_%H_%M_%S')
                print(object_name)
                
                save_object(get_user_id(username.value),object,object_name)
                
                object_id = get_obj_id(get_user_id(username.value),object_name)

                obj_name = "Custom:" + str(object_id) + "-" + custom_object_name.value
                
                object_type.options.append(ft.dropdown.Option(obj_name,on_click= add_custom_ui)) # saved locally via list
               
                obj_error_message.value = "Object saved and can be accessed in object type"
                obj_error_message.visible = True
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

        
        
        def add_texture_ui(e):  #e is the event object of the texture dropdown
            texture = e.control.value  #name of the texture selected 
            
            if texture == "Image":
                double_colour_texture_buttons.visible = False
                colour_button.visible = False
                image_texture_button.visible = True

                
            
            elif texture == "None":
                texture_type.value = None
                double_colour_texture_buttons.visible = False
                image_texture_button.visible = False
                colour_button.visible = True
                
            else:
                colour_button.visible = False
                image_texture_button.visible = False
                double_colour_texture_buttons.visible = True
   
            page.update()
                
                

        
        def add_material(material): 
            material_tile.visible = False
            
         
            
            material_coeffs = {
                "Plastic": [0.6,0.2,0.2,0.0],
                "Matte" : [0.8,0.1,0.1,0.0],
                "Glossy" : [0.8,0.5,0.1,0.3],
                "Metal": [0.2, 0.9, 0.1, 0.8],
                "Mirror": [0.0, 1.0, 0.0, 1.0],
                "Glass": [0.1, 0.6, 0.1, 0.9],  # Not refractive yet, but reflectivity mimics gloss
                "Rubber": [0.9, 0.1, 0.1, 0.05],
                "Ceramic": [0.7, 0.3, 0.2, 0.2],

                }
            
            print(f"the material is {material}")
            Diffuse_input.text_field.value = str(material_coeffs[material][0])
            Specular_input.text_field.value = str(material_coeffs[material][1])
            Ambient_input.text_field.value = str(material_coeffs[material][2])
            reflectivity_input.text_field.value = str(material_coeffs[material][3])
            
           
                
            
            
            page.update()


        def add_material_tile(e):
            material_tile.visible = True
            page.update()

        def remove_material_tile(e):
            material_tile.visible = False
            material_type.value = None
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
        
        
        
        
        def render(e):
            print(f"the top control is {page.controls[0]} ")

            if img.src:
                page.controls.pop(0)
                img.src = None

            img.src = None
            page.update()  # clear the image preview first

            global scene_name
            print(f"the scene name is {scene_name}")
            if scene_name is None:
                scene_name = "image"

            timestamp = datetime.today().strftime('%Y-%m-%d_%H_%M_%S')
            scene_name_png = scene_name + timestamp + ".png"
            scene_name_ppm = scene_name + timestamp + ".ppm"

            current_name.value = f"Current Name: {scene_name}"

            if final_validation() is False:
                return

            scene_error_message.visible = False
            pb.visible = True
            est_time.value = "Estimated Time: 0s"
            est_time.visible = True
            pb.value = 0
            page.update()  

            
            def do_render():
                scene_width = int(width_input.value)
                scene_height = int(height_input.value)
                global user_scene
                user_scene = Scene(scene_objects, scene_camera, scene_width, scene_height, lights)

                Engine = engine()
                start_time = time.time()
                
                def progress_callback(progress):
                    elapsed = time.time() - start_time

                    if progress > 0:
                        estimated_total_time = elapsed / progress
                        time_left = estimated_total_time - elapsed
                        est_time.value = f"Estimated Time Left: {int(time_left)}s"
                    else:
                        est_time.value = "Estimating..."

                    pb.value = progress
                    page.update()

                image = Engine.render(user_scene, progress_callback=progress_callback)

                with open(scene_name_ppm, "w") as img_file:
                    image.write_ppm(img_file)

                convert_ppm_to_png(scene_name_ppm, scene_name_png)
                os.remove(scene_name_ppm)

                if User_Status:
                    target_path = f"User_Data/{get_user_id(username.value)}/{scene_name_png}"
                    os.rename(scene_name_png, target_path)
                    img.src = target_path
                else:
                    img.src = scene_name_png


                img_viewer.content = img
                page.controls.insert(0, img_tile)
                img.visible = True
                pb.visible = False
                est_time.visible = False
                pb.value = 0
                page.update()

            
            threading.Thread(target=do_render, daemon=True).start()


                
        
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
                
                page.update()
            
            
            img_viewer.content = img
            page.controls.insert(0, img_tile)
            pb.visible = False
            img.visible = True
            
            pb.value = 0

            page.update()

        
        def autofill(e):  #on click method for the Autofill Button used to fill example test values for scene
            render_name.value = "Testy"
            light_pos.value = "0,0,0"
            cam_pos.value = "0,-1,0"
            width_input.value = "300"
            height_input.value = "200"
            object_position.value = "0,5,0"
            object_radius.value = "1.0"
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
            global saved_scene_data
            saved_scene_data = None
            page.controls.clear()
            username.value = ""
            password.value = ""
            loginpage()
            page.update()
        
        
        

        def load_custom_objects_to_ui():
            if User_Status:
                custom_objects = load_objects(get_user_id(username.value))
                for obj in custom_objects:
                    
                    object_type.options.append(ft.dropdown.Option(f"Custom:{obj[0]}-{obj[1][:-19]}",on_click= add_custom_ui))
                page.update()
                        
        img_carousel = ft.Row(expand=1, wrap=False, scroll="always")
        
        def edit(src):
            img.src = src
            img_viewer.content = img
            img.visible = True
            
            img_showcaser(e)
        
        def my_renders(e):
            page.controls.clear()
            global page_tracker
            page_tracker = "my_renders"
            scenes = get_scenes(get_user_id(username.value))  
            scenes = scenes[-1::-1]     #stack

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
            colour_button.visible = False
            
            material_type.visible = False
            texture_type.visible = False
            page.update()
        
        def add_floor_ui(e):
            remove_ui()
            page.update()

        def add_Array_ui(e):
            remove_ui()

            number.visible = True
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

        def add_Cube_ui(e):
            remove_ui()
            object_position.visible = True
            object_position.label = "Cube Center Position"
            object_radius.visible = True
            object_radius.label = "Cube Side Length"
            object_rotation.visible = True
            page.update()

        def remove_ui():
            material_type.visible = True
            texture_type.visible = True
            colour_button.visible = True
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

    
        
        number = IntField("Number of objects",1,1000,1,1)
        number.visible = False
        render_name = ft.TextField(label="Render Name",hint_text="e.g., My_Render", width=600,border_color=ft.colors.GREEN_800)
        light_pos = ft.TextField(label="Light Source Postion",hint_text="e.g. x, y, z", width=325,border_color=ft.colors.GREEN_800)
        brightness_slider = ft.Slider(min=0,value = 1, max=1, divisions=10,round=1,label="Brightness: {value}",width=400)
        cam_pos = ft.TextField(label= "Camera Postion",hint_text="e.g. x, y, z", width=300,border_color=ft.colors.GREEN_800)
        fov_slider = ft.Slider(min=20,value = 90, max=150, divisions=130,label="FOV: {value}",width=400)
        
        brightness_tile = ft.Column(
            [ft.Text("Light Brightness"),brightness_slider],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=1,
        )
        
        fov_tile = ft.Column(
            [ft.Text("Camera FOV"),fov_slider],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=1,
        )


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
                     ft.dropdown.Option("Cube",on_click= add_Cube_ui),
                     ft.dropdown.Option("Tetrahedron",on_click= add_Sphere_ui),
                    ft.dropdown.Option("Capsule",on_click= add_Cylinder_ui),
                    ft.dropdown.Option("Array",on_click= add_Array_ui),

                     ],
            width=150,
            border_color= ft.colors.GREEN_800,
        )

        load_custom_objects_to_ui()
   
        est_time = ft.Text("Estimated Time: ")
        est_time.visible = False
        pb = ft.ProgressBar(width=400)
        pb.visible = False
        
        set = MyButton(text="Set", on_click=set_name)
        
        object_position = ft.TextField(label="Object Position", hint_text="e.g., (x, y, z)", width=150,border_color=ft.colors.GREEN_800)
        object_radius = ft.TextField(label="Object Radius", hint_text="e.g., 0.5", width=150,border_color=ft.colors.GREEN_800)
        object_rotation = ft.TextField(label="Object Rotation", hint_text="e.g., (0, 45, 0) in degrees", width=150,border_color=ft.colors.GREEN_800)
        
        cone_axis = ft.TextField(label="Cone Axis", hint_text="e.g., (x, y, z)", width=150,border_color=ft.colors.GREEN_800)
        cone_angle = ft.TextField(label="Cone Angle", hint_text="e.g., 45", width=150,border_color=ft.colors.GREEN_800)
        cone_axis.visible = False
        cone_angle.visible = False
        object_rotation.visible = False

        object_abc = ft.Row(
            [
            IntField("X radius",0,100,1,1),
            IntField("Y radius",0,100,1,1),
            IntField("Z radius",0,100,1,1),]
        )
        
        object_abc.visible = False

        cylinder_allignment = ft.Dropdown(
            label="Cylinder Allignment",
            options=[ft.dropdown.Option("Horizontal(X)"),
                     ft.dropdown.Option("Forward(y)"),
                     ft.dropdown.Option("Vertical(z)"),
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
            options=[(ft.dropdown.Option("Plastic",on_click= lambda e: add_material("Plastic") ) ) , 
                    (ft.dropdown.Option("Matte",on_click= lambda e: add_material("Matte") ) ),
                    (ft.dropdown.Option("Glossy",on_click= lambda e: add_material("Glossy") ) ),
                    (ft.dropdown.Option("Metal",on_click= lambda e: add_material("Metal") ) ),
                    (ft.dropdown.Option("Mirror",on_click= lambda e: add_material("Mirror") ) ),
                    (ft.dropdown.Option("Glass",on_click= lambda e: add_material("Glass") ) ),
                    (ft.dropdown.Option("Rubber",on_click= lambda e: add_material("Rubber") ) ),
                    (ft.dropdown.Option("Ceramic",on_click= lambda e: add_material("Ceramic") ) ), 
                    (ft.dropdown.Option("Custom", on_click= add_material_tile)),
                    (ft.dropdown.Option("None", on_click= remove_material_tile))],
            width=150,
            border_color= ft.colors.GREEN_800,

        )
        
        texture_type = ft.Dropdown(
            label= "Texture Type",
            options=[(ft.dropdown.Option("Checker") ) ,
                     (ft.dropdown.Option("Gradient") ) , 
                     (ft.dropdown.Option("Noise") ) ,
                     (ft.dropdown.Option("Wood") ) ,
                     (ft.dropdown.Option("Marble") ),
                     (ft.dropdown.Option("Smoke") ),
                     (ft.dropdown.Option("Stripes") ),
                     (ft.dropdown.Option("Radial") ),
                     (ft.dropdown.Option("Brick") ),
                     (ft.dropdown.Option("Image") ),
                     (ft.dropdown.Option("None") ) ,
                    ],
            width=150,
            border_color= ft.colors.GREEN_800,
            on_change=add_texture_ui,
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

        
        def pick_files_result(e: FilePickerResultEvent):
            if e.files:
                file = e.files[0]
                selected_image_texture_file.value = f"Selected image: {file.name}"
                selected_image_texture_file_path.value = file.path
                
            else:
                selected_image_texture_file.value = "No file selected"
                selected_image_texture_file_path.value = None
            
            selected_image_texture_file.update()
        
        
        
        pick_files_dialog = FilePicker(on_result=pick_files_result)
        selected_image_texture_file = ft.Text()
        selected_image_texture_file_path = ft.Text()
        selected_image_texture_file_path.visible = False
        page.overlay.append(pick_files_dialog)

        
        
        image_texture_button = ft.Row(
            [
                ft.ElevatedButton(
                    "Pick image",
                    icon=ft.icons.UPLOAD_FILE,
                    on_click=lambda _: pick_files_dialog.pick_files(
                        allow_multiple=False,
                        allowed_extensions=["png", "jpg", "jpeg", "bmp", "gif", "webp"]
                    ),
                ),
                selected_image_texture_file,
            ]
        )
       
        image_texture_button.visible = False

       
        
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
            if User_Status:
                    remove_img_from_library(img.src)
                    
            os.remove(img.src)            
            img.src = None
            page.controls.pop(0)
           
            if page_tracker != "main":
                switch_to_main_ui(e)
            page.update()
        
        
        def img_to_library(e):
            
            
            scene_data = get_scene_data(user_scene)
            userID = get_user_id(username.value)
            
            create_scene(userID,img.src,scene_name,scene_data)

            page.add(ft.Text(f"{scene_name} added to library"))
            page.update()
            


        def reload_scene(img_path):
            
            global saved_scene_data
            saved_scene_data = get_scene_data_from_db(img_path)
            print(f"the saved scene data is {saved_scene_data}")
            
            switch_to_main_ui(e)

            

            
            
            


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
            global page_tracker
            print(f"the page tracker is {page_tracker}")
            print("the image is ",img.src)
            
            if User_Status and page_tracker == "my_renders":
                page.add(
                    theme_switch_button,
                    img_viewer,
                    ft.Row([
                        
                        ft.IconButton(icon=ft.icons.DOWNLOAD ,tooltip= "download", on_click=lambda e: download_file(img.src)),
                        ft.IconButton(icon=ft.icons.DELETE ,tooltip= "delete", on_click=remove_img),
                        ft.IconButton(icon=ft.icons.CONTENT_COPY ,tooltip= "Copy", on_click= lambda e: copy_image_to_clipboard(img.src)),
                        ft.IconButton(icon=ft.icons.BUILD ,tooltip= "Modify Scene", on_click=lambda e : reload_scene(img.src)),],    
                    alignment=ft.MainAxisAlignment.CENTER,
                    ),
                    
                    main_menu_Button,
                    Sign_out_Button,
                    

                )
                page.update()
                
           
            elif User_Status:
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
                        ft.IconButton(icon=ft.icons.DELETE ,tooltip= "delete", on_click=remove_img), ],
                    
                    alignment=ft.MainAxisAlignment.CENTER,
                    ),
                    main_menu_Button,
                    Sign_out_Button,
                )
                page.update()
            
            
            page_tracker = "showcaser"
            
        
        
        
        img_viewer= ft.InteractiveViewer(
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
                number,
                object_position,
                object_abc,
                cylinder_allignment,
                cone_axis,
                cone_angle,
                object_radius,  #sometimes height
                cylinder_radius,
                object_rotation,
                stopper,
                material_tile,
                material_type,
                ft.Column([texture_type,double_colour_texture_buttons,image_texture_button]),
                colour_button,
                add_object_button,
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=10,
        )
   
      


        page.add(
            
            pb,
            est_time,
            theme_switch_button,
            ft.Column(
                [
                    ft.Row(
                        [render_name,set], alignment=ft.MainAxisAlignment.CENTER
                        
                    ),
                    name_error_message,
                    current_name,
                    ft.Row(
                        [light_pos,brightness_tile,add_light_button], alignment=ft.MainAxisAlignment.CENTER
                        
                    ),
                    light_error_message,
                    ft.Text("Added Lights:"),
                    added_lights,
                    
                    ft.Row(
                        [cam_pos,fov_tile,add_cam_button], alignment=ft.MainAxisAlignment.CENTER
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
                    ft.Row([R_Button(text="Auto Fill", on_click=autofill)], alignment=ft.MainAxisAlignment.CENTER),
                    
                
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
                    
                    ft.Text(
                    "Password must contain at least :\n- 8 characters\n- One capital letter\n- One special character (!, @, $, %, ^, &, *, +, #)\n- One number",
                    size=12,
                    color=ft.colors.GREY,
                    italic=True,
                    weight=ft.FontWeight.BOLD,
                    text_align=ft.TextAlign.CENTER,
                    ),

                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            )
        )



        page.update()

    loginpage()

ft.app(main)

