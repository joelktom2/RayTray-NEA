from image import colour
from Maths import Vector
from objects import Sphere,camera
from engine import engine
import flet as ft
from tkinter import Tk, colorchooser
from scene import Scene
from PIL import Image





def main(page):
    page.title = "Renderer"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

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


        # Render UI (updated content)
        class MyButton(ft.ElevatedButton):
            def __init__(self, text, on_click):
                super().__init__()
                self.bgcolor = ft.colors.GREEN_100
                self.color = ft.colors.GREEN_800
                self.text = text
                self.on_click = on_click

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

        # List to hold added objects
        added_objects = ft.Column(spacing=5)

        
        #scene data initialization
        scene_objects = []

        
        

        def add_object(e):
            if object_type.value and object_position.value and selected_color and object_radius.value:
                added_objects.controls.append(
                    ft.Text(f"Type: {object_type.value},Radius {object_radius.value}, Position: {object_position.value}, Color: {selected_color}")
                )
                position_parts = object_position.value.split(",")
                x, y, z = map(int, position_parts)
                myobj1 = Sphere(Vector(x, y, z), float(object_radius.value), colour.hex_to_rgb(selected_color))
                scene_objects.append(myobj1)
                
                page.update()

        def update_dimensions(e):
            current_width.value = f"Current Width: {width_input.value}"
            current_height.value = f"Current Height: {height_input.value}"
            page.update()
            

        def pick_color(e):
            # Use Tkinter color chooser
            root = Tk()
            root.lift()  # Bring the Tkinter root window to the front
            root.attributes("-topmost", True)  # Ensure it's on top
            root.withdraw()  # Hide the root window
            color_code = colorchooser.askcolor(title="Choose a color")[1]
            root.destroy()  # Destroy the root window
            if color_code:
                nonlocal selected_color
                selected_color = color_code
                color_picker_button.text = f"Selected: {selected_color}" 
                color_picker_button.bgcolor = selected_color 
                page.update()

        def convert_ppm_to_png(ppm_path, png_path):
            with open(ppm_path, "rb") as f:
                image = Image.open(f)
                image.save(png_path, "PNG")
        
        def render(e):
            
            cam_parts = cam_pos.value.split(",")
            x, y, z = map(int, cam_parts)
            scene_camera = camera(Vector(x, y, z))
            scene_width = int(width_input.value)
            scene_height = int(height_input.value)
            

            user_scene = Scene(scene_objects,scene_camera,scene_width,scene_height)  
            Engine = engine()
            image = Engine.render(user_scene)
            with open("image.ppm", "w") as img_file:
                image.write_ppm(img_file)
                
            convert_ppm_to_png("image.ppm", "image.png")
            img.src = "image.png"
            img.visible = True
            img.update()

                
        
        selected_color = None  # Holds the selected color

        cam_pos = ft.TextField(hint_text="Camera Position", width=600)
        width_input = ft.TextField(hint_text="Width", width=200, on_change=update_dimensions)
        height_input = ft.TextField(hint_text="Height", width=200, on_change=update_dimensions)

        current_width = ft.Text("Current Width: ")
        current_height = ft.Text("Current Height: ")

        # Object section
        object_type = ft.Dropdown(
            label="Object Type",
            options=[ft.dropdown.Option("Sphere")],
            width=300,
        )
        object_position = ft.TextField(label="Object Position", hint_text="e.g., (x, y, z)", width=300)
        object_radius = ft.TextField(label="Object Radius", hint_text="e.g., 0.5", width=300)
        color_picker_button = MyButton(text="Pick Color", on_click=pick_color)
        add_object_button = MyButton(text="Add Object", on_click=add_object)

        # Add the updated render UI
        page.add(
            img,
            ft.Column(
                [
                    ft.Row([cam_pos], alignment=ft.MainAxisAlignment.CENTER),
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
    login_button = ft.ElevatedButton(text="Login", on_click=switch_to_main_ui)

    page.add(
        ft.Column(
            [
                ft.Text("Welcome to RayTray", size=20, weight=ft.FontWeight.BOLD),
                username,
                password,
                login_button,
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )
    )


ft.app(main)
