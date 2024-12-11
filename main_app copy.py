from image import colour
from Maths import Vector
from objects import Sphere
from engine import engine
import flet as ft
from tkinter import Tk, colorchooser
from scene import Scene,camera
from PIL import Image
from light import light
from loginsys import hash_password,verify_password,create_user,login_user
import re


def main(page):
    page.title = "Renderer"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    
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

    

    def register(e):
        usern = username.value
        pwd = password.value
        if not usern or not pwd:
            error_message.value = "Invalid username or password"
            error_message.visible = True
            print("here")
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
        switch_to_main_ui(e)   #switches to the main UI when the user logs in successfully
    
    
    def switch_to_main_ui(e):
        
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
            if re.fullmatch(r'-?\d+,-?\d+,-?\d+', value):
                return True
            return False
        
    
        added_objects = ft.Column(spacing=5)
        added_lights = ft.Column(spacing=5)
        
        #scene data initialization
        scene_objects = []
        lights = []
        
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
        
        def add_object(e):   #adds an object to the scene
            if object_type.value and object_position.value and selected_color and object_radius.value:
                position_parts = object_position.value.split(",")
                x, y, z = map(int, position_parts)
                myobj1 = Sphere(Vector(x, y, z), float(object_radius.value), colour.hex_to_rgb(selected_color))
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
            

        def pick_color(e):   #presents a color picker to the user
            
            root = Tk()
            root.lift()  # Brings the Tkinter root window to the front
            root.attributes("-topmost", True)  # Ensure it's on top
            root.withdraw()  
            color_code = colorchooser.askcolor(title="Choose a color")[1]
            root.destroy()  
            if color_code:
                nonlocal selected_color
                selected_color = color_code
                color_picker_button.text = f"Selected: {selected_color}" 
                color_picker_button.bgcolor = selected_color 
                page.update()

        def convert_ppm_to_png(ppm_path, png_path): #Used to convert the rendered image to a png format
            with open(ppm_path, "rb") as f:
                image = Image.open(f)
                image.save(png_path, "PNG")
        
        def render(e):   #renders the scene
            
            cam_parts = cam_pos.value.split(",")
            x, y, z = map(int, cam_parts)
            scene_camera = camera(Vector(x, y, z))
            scene_width = int(width_input.value)
            scene_height = int(height_input.value)
            user_scene = Scene(scene_objects,scene_camera,scene_width,scene_height,lights)  
            Engine = engine()
            image = Engine.render(user_scene)
            with open("image.ppm", "w") as img_file:
                image.write_ppm(img_file)
                
            convert_ppm_to_png("image.ppm", "image.png")
            img.src = "image.png"
            img.visible = True
            img.update()

                
        
        selected_color = None  # Holds the selected color

        light_pos = ft.TextField(hint_text="Light Source", width=600)
        cam_pos = ft.TextField(hint_text="Camera Position", width=600)
        width_input = ft.TextField(hint_text="Width", width=200, on_change=update_dimensions)
        height_input = ft.TextField(hint_text="Height", width=200, on_change=update_dimensions)

        current_width = ft.Text("Current Width: ")
        current_height = ft.Text("Current Height: ")

        object_type = ft.Dropdown(
            label="Object Type",
            options=[ft.dropdown.Option("Sphere")],
            width=300,
        )
        object_position = ft.TextField(label="Object Position", hint_text="e.g., (x, y, z)", width=300)
        object_radius = ft.TextField(label="Object Radius", hint_text="e.g., 0.5", width=300)
        color_picker_button = MyButton(text="Pick Color", on_click=pick_color)
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

    
        
        
        
        page.add(
            img,
            ft.Column(
                [
                    ft.Row(
                        [light_pos,add_light_button], alignment=ft.MainAxisAlignment.CENTER
                        
                    ),
                    light_error_message,
                    ft.Text("Added Lights:"),
                    added_lights,
                    
                    ft.Row([cam_pos], alignment=ft.MainAxisAlignment.CENTER),
                    cam_error_message,
                    ft.Row([width_input, height_input], alignment=ft.MainAxisAlignment.CENTER),
                    ft.Row([current_width, current_height], alignment=ft.MainAxisAlignment.CENTER),
                    ft.Text("Objects", size=16, weight=ft.FontWeight.BOLD),
                    ft.Row(
                        [
                            object_type,
                            object_position,
                            object_radius,
                            color_picker_button,
                            add_object_button,
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        spacing=10,
                    ),
                    ft.Text("Added Objects:"),
                    added_objects,  # Display added objects
                    ft.Row([R_Button(text="Render", on_click=render)], alignment=ft.MainAxisAlignment.CENTER),
                    
                ],
                alignment=ft.MainAxisAlignment.CENTER,  # Center vertically
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,  # Center horizontally
            )
        )
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

            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )
    )


ft.app(main)
