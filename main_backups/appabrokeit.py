#My libraries
from image import colour
from Maths import Vector
from objects import Sphere
from engine import engine
from scene import Scene,camera
from light import light
from loginsys import create_user,login_user,get_user_id
from scenes_table import create_scene,get_scenes,get_scene_names,remove_scene


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
from time import time  # Add this import at the top of the file
from datetime import datetime


def main(page):
    page.title = "RayTray"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    
    global User_Status  
    User_Status = None
    
    def username_sanitate(value):
        if re.fullmatch(r'[A-Za-z0-9#_]+', value):
            return True
        return False   #checks if the username is valid
    
    def password_sanitate(value):
    
        allowed_special_characters = r"~`!@#$%^&*()+=_\-{}[\]\\|:;”’?/<>,."
        pattern = rf"[A-Za-z0-9{re.escape(allowed_special_characters)}]+"
        if re.fullmatch(pattern, value):
            return True
        return False     #checks if the password is valid

    def guest(e):
        global User_Status
        User_Status = False
        error_message.visible = False
        switch_to_main_ui(e)

    def register(e):
        usern = username.value
        pwd = password.value
        if not usern or not pwd:
            error_message.value = "Invalid username or password"
            error_message.visible = True
            
            page.update()
            return
        #input sanitation
        if not username_sanitate(usern) or not password_sanitate(pwd):
            error_message.value = "Invalid username or password"
            error_message.visible = True
            page.update()
            return
        
        page.update()
        create_user(usern,pwd)
        
        path = f'C:/Users/jobyk/python/RayTray - NEA/User_Data/{get_user_id(usern)}' 
        if not os.path.exists(path):
            os.makedirs(path)
        
        
        
        global User_Status
        User_Status = True

        

        switch_to_main_ui(e)
    
    def login(e):
        
        
        usern = str(username.value)
        pwd = str(password.value)
        #input sanitation
        if not usern or not pwd:
            error_message.value = "Invalid username or password"
            error_message.visible = True
            page.update()
            return
        if not username_sanitate(usern) or not password_sanitate(pwd):
            error_message.value = "Invalid username or password"
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
        
        global names
        names = [row[0] for row in (get_scene_names(get_user_id(usern)))]

        
        switch_to_main_ui(e)   #switches to the main UI when the user logs in successfully
    
    
    def switch_to_main_ui(e):
        page_tracker = "main"
        
        error_message.visible = False
        
        
        
        
        
        
        # Clear the login page
        page.controls.clear()
        
        img = ft.Image(
            src=None,  # Initialize with no image source
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
                self.width = 800
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
                x, y, z = map(float, position_parts)
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
                cam_error_message.visible = False
                cam_parts = cam_pos.value.split(",")
                x, y, z = map(float, cam_parts)
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
        
        
        
        
        
        
        def add_object(e):   #adds an object to the scene
            
            if validcoord(object_position.value) == False:
                obj_error_message.value = "Please enter a valid position"
                obj_error_message.visible = True
                page.update()
            elif object_type.value == None:
                obj_error_message.value = "Please select an object type"
                obj_error_message.visible = True
                page.update()

            elif validradius(object_radius.value) == False:
                obj_error_message.value = "Please enter a valid radius"
                obj_error_message.visible = True
                page.update()
            
            elif selected_color == None:
                obj_error_message.value = "Please select a color"
                obj_error_message.visible = True
                page.update()
            #object_type.value and object_position.value and selected_color and object_radius.value:
            else: 
                obj_error_message.visible = False
                
                position_parts = object_position.value.split(",")
                x, y, z = map(float, position_parts)
                obj_material = [float(Diffuse_input.text_field.value),float(Specular_input.text_field.value),float(Ambient_input.text_field.value)] 
                
                myobj1 = Sphere(Vector(x, y, z), float(object_radius.value), colour.hex_to_rgb(selected_color),obj_material)
                
                scene_objects.append(myobj1)
                
                
                added_objects.controls.append(
                    ft.Row(
                        [(ft.Text(f"Type: {object_type.value},Radius {object_radius.value}, Position: {object_position.value}, Color: {selected_color}")),Remove_ButtonLite(text="Remove", on_click=lambda e: remove_object(e, myobj1))] , alignment=ft.MainAxisAlignment.CENTER
                        
                    ),
                
                )
                
                page.update()

        def remove_object(e, object):  #removes object from the scene
            onum = scene_objects.index(object)
            scene_objects.pop(onum)
            added_objects.controls.pop(onum)
            page.update()
        
        
        def update_dimensions(e):   #updates the dimensions of the scene dynamically 
            current_width.value = f"Current Width: {width_input.value}"
            current_height.value = f"Current Height: {height_input.value}"
            page.update()
        

        
        def minus_click(text_field,mininum):
            value = round(float(text_field.value) - 0.1, 1)
            if value < mininum:
                obj_error_message.value = "Coefficients must be between 0.0 and 1.0"
                obj_error_message.visible = True
            else:
                obj_error_message.visible = False
                text_field.value = str(value)
            
            page.update()
        
        
        def plus_click(text_field,maximum):
            value = round(float(text_field.value) + 0.1, 1)
            if value > maximum:
                obj_error_message.value = "Coefficients must be between 0.0 and 1.0"
                obj_error_message.visible = True
            else:
                obj_error_message.visible = False
                text_field.value = str(value)
            
            page.update()

        class IntField(ft.Container):
            def __init__(self,name,min,max,default="0.0"):
                super().__init__()
                self.text_field = ft.TextField(
                    label=str(name),
                    value=default,
                    text_align=ft.TextAlign.RIGHT,
                    width=80
                )
                self.content = ft.Row(
                    [
                        ft.IconButton(
                            icon=ft.icons.REMOVE, 
                            on_click=lambda e: minus_click(self.text_field,min),
                            icon_size=20,
                            padding= 1
                        ),
                        self.text_field,
                        ft.IconButton(
                            icon=ft.icons.ADD, 
                            on_click=lambda e: plus_click(self.text_field,max),
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
        
        
        # def render(e):   #renders the scene
        #     if User_Status:
        #         global names
        #         names = [row[0] for row in (get_scene_names(get_user_id(username.value)))]
            
        #     print(f"the top control is {page.controls[0]} ")
            
        #     if img.src:
        #         page.controls.pop(0)
        #         img.src = None
            
        #     img.src = None
        #     page.update()
            
        #     global scene_name
        #     print(f"the scene name is {scene_name}")
            
        #     if scene_name == None:
        #         scene_name = "image"
            
        #     print(f"the names are {names}")
        #     while scene_name in names:
        #         scene_name = scene_name + "#"

        #     scene_name_png = scene_name + +".png"
        #     scene_name_ppm = scene_name + ".ppm"
            
        #     current_name.value = f"Current Name: {scene_name}"

        #     if final_validation() == False:
        #         pass
        #     else:
        #         scene_error_message.visible = False
        #         pb.visible = True
        #         pb.value = 0
                
        #         scene_width = int(width_input.value)
        #         scene_height = int(height_input.value)
        #         user_scene = Scene(scene_objects,scene_camera,scene_width,scene_height,lights)  
                
        #         Engine = engine()
        #         image = Engine.render(user_scene)
        #         with open(scene_name_ppm, "w") as img_file:
        #             image.write_ppm(img_file)

        #         convert_ppm_to_png(scene_name_ppm, scene_name_png)
                
        #         os.remove(scene_name_ppm)   #deletes the ppm file after conversion

        #         print(f"User : {User_Status}")
                
        #         if User_Status:
        #             os.rename(scene_name_png, f"User_Data/{get_user_id(username.value)}/{scene_name_png}")
        #             img.src = f"User_Data/{get_user_id(username.value)}/{scene_name_png}?t={int(time())}"
        #         else:
        #             img.src = f"{scene_name_png}?t={int(time())}"
        #             print(img.src)
                
                
        #         page.update()
                
        #         print("######################")
        #         for i in range(0, 101):    #loading a progress bar not accurate of the rendering speed but for decoration
        #             pb.value = i * 0.02
        #             sleep(0.01)
        #             page.update()
                  
                
                
        #         page.controls.insert(0, img_tile)
                
        #         img.visible = True
                
        #         page.update()
        #         img.update()
        #         img_viewer.update()
        #         img_tile.update()
        #         pb.visible = False
        #         pb.value = 0
                
                
                
        #         page.update()

        def render(e):  # Renders the scene
            global scene_name, names
            
            # Update the scene names if the user is logged in
            if User_Status:
                user_id = get_user_id(username.value)
                names = [row[0] for row in get_scene_names(user_id)]
            else:
                names = []
            
            print(f"The top control is {page.controls[0]}")

            # Clear previous image if exists
            if img.src:
                page.controls.pop(0)
                img.src = None
                page.update()

            scene_name_ts = ""
            scene_name = scene_name or "image"

            # Add timestamp to the scene name
            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
            
            if User_Status:
                scene_name_ts = f"{scene_name}_{user_id}_{timestamp}"
            else:
                scene_name_ts = f"{scene_name}_{timestamp}"

            while scene_name in names:
                scene_name += "#"

            scene_name_png = f"{scene_name_ts}.png"
            scene_name_ppm = f"{scene_name_ts}.ppm"
            

            current_name.value = f"Current Name: {scene_name}"
            print(f"Scene name: {scene_name}")
            print(f"Scene names: {names}")

            if not final_validation():
                return

            # Prepare for rendering
            scene_error_message.visible = False
            pb.visible = True
            pb.value = 0

            scene_width = int(width_input.value)
            scene_height = int(height_input.value)
            user_scene = Scene(scene_objects, scene_camera, scene_width, scene_height, lights)

            # Render the scene
            Engine = engine()
            image = Engine.render(user_scene)
            with open(scene_name_ppm, "w") as img_file:
                image.write_ppm(img_file)

            convert_ppm_to_png(scene_name_ppm, scene_name_png)
            os.remove(scene_name_ppm)  # Delete the PPM file after conversion

            print(f"User: {User_Status}")

            #Save image to user directory if logged in
            if User_Status:
                user_dir = f"User_Data/{user_id}"
                os.rename(scene_name_png, f"{user_dir}/{scene_name_png}")
                img.src = f"{user_dir}/{scene_name_png}"
            else:
                img.src = scene_name_png
            
            img.src = scene_name_png
            print(img.src)
            img_viewer.content = img

            # Show loading progress bar (decorative)
            for i in range(101):
                pb.value = i * 0.02
                sleep(0.01)
                page.update()

            # Update UI with the rendered image
            
            
            page.controls.insert(0, img_tile)
            img.visible = True
            page.update()
            img.update()
            img_viewer.update()
            img_tile.update()

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

        
        
        
        
        def validate_name(value):   #validates the name of the render
            if re.fullmatch(r'[A-Za-z0-9#_]+', value):
                return True
            return False
        
        def set_name(e):   #sets the name of the render
            if validate_name(render_name.value):
                name_error_message.visible = False
                
                
                if User_Status:
                    global names
                    names = [row[0] for row in (get_scene_names(get_user_id(username.value)))]
                    print(names)
                
                    while render_name.value in names:
                        render_name.value = render_name.value + "#"
                
                
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
            print(f"the image paths are {image_paths}")
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
        selected_color = None  # Holds the selected color
        
        
        
        
        
        
        
        render_name = ft.TextField(label="Render Name",hint_text="e.g., My_Render", width=600,)
        light_pos = ft.TextField(label="Light Source Postion",hint_text="e.g., (x, y, z)", width=600)
        cam_pos = ft.TextField(label= "Camera Postion",hint_text="e.g., (x, y, z)", width=600)
        width_input = ft.TextField(label = "Width",hint_text="e.g., 300", width=200, on_change=update_dimensions)
        height_input = ft.TextField(label = "height",hint_text="e.g., 200", width=200, on_change=update_dimensions)

        current_width = ft.Text("Current Width: ")
        current_height = ft.Text("Current Height: ")
        current_name = ft.Text("Current Name: ")

        object_type = ft.Dropdown(
            label="Object Type",
            options=[ft.dropdown.Option("Sphere")],
            width=150,
        )
        pb = ft.ProgressBar(width=400)
        pb.visible = False
        set = MyButton(text="Set", on_click=set_name)
        object_position = ft.TextField(label="Object Position", hint_text="e.g., (x, y, z)", width=150)
        object_radius = ft.TextField(label="Object Radius", hint_text="e.g., 0.5", width=150)
        Ambient_input = IntField("Ambient",0,1)
        Diffuse_input = IntField("Diffuse",0,1,0.5)
        Specular_input = IntField("Specular",0,1,0.5)
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

        def pick_color():
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
                global selected_color
                selected_color = color_picker.color
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
                global names
                names = [row[0] for row in (get_scene_names(get_user_id(username.value)))]
                if scene_name in names:
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
                # Open the image file
                image = Image.open(image_path)

                # Convert the image to BMP format for clipboard compatibility
                output = io.BytesIO()
                image.convert("RGB").save(output, "BMP")
                bmp_data = output.getvalue()[14:]  # Remove the BMP header
                output.close()

                # Open clipboard and set the image data
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

        
        
        
      


        page.add(
            
            pb,
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
                    ft.Row(
                        [
                            object_type,
                            object_position,
                            object_radius,
                            Diffuse_input,
                            Specular_input,
                            Ambient_input,

                            pick_color(),
                            add_object_button,
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        spacing=10,
                    ),
                    obj_error_message,
                    ft.Text("Added Objects:"),
                    added_objects,  # Display added objects
                    ft.Row([R_Button(text="Render", on_click=render)], alignment=ft.MainAxisAlignment.CENTER),
                    scene_error_message,
                    ft.Row([Sign_out_Button,R_Button(text="Test Render", on_click=test_render),My_Renders_Button], alignment=ft.MainAxisAlignment.CENTER),
                    
                    
                
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
    username = ft.TextField(label="Username", width=300)
    password = ft.TextField(label="Password", password=True, width=300)
    
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

