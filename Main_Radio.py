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
from time import sleep
import os

#radio_setup
current_dir = os.path.dirname(os.path.abspath(__file__))
radio_folder = os.path.join(current_dir, "Radio")
global song_index
song_index = 0
playlist = [f for f in os.listdir(radio_folder) if f.endswith(".mp3")]
print(playlist)
audio_file = os.path.join(radio_folder, playlist[song_index])
audio = ft.Audio(src=audio_file, autoplay=False)



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
            if re.fullmatch(r'-?\d+,-?\d+,-?\d+', value):
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
        def update_name(e):   #updates the name of the render dynamically
            current_name.value = f"Current Name: {render_name.value}"
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
            print(page.controls[0])
            
            if img.src:
                page.controls.pop(0)
                img.src = None
            
            img.src = None

            page.update()
            
            
            global scene_name
            if scene_name == None:
                scene_name = "image.ppm"
                scene_name_png = "image.png"
            else:
                scene_name_png = scene_name + ".png"
                scene_name = scene_name + ".ppm"

            if validlength(width_input.value) == False or validlength(height_input.value) == False:
                scene_error_message.value = "Please enter valid dimensions of the scene "
                scene_error_message.visible = True
                page.update()
                return
            else:
                scene_error_message.visible = False
                pb.visible = True
                pb.value = 0
                
                scene_width = int(width_input.value)
                scene_height = int(height_input.value)
                user_scene = Scene(scene_objects,scene_camera,scene_width,scene_height,lights)  
                
                Engine = engine()
                image = Engine.render(user_scene)
                with open(scene_name, "w") as img_file:
                    image.write_ppm(img_file)

                convert_ppm_to_png(scene_name, scene_name_png)
                
                img.src = scene_name_png
                
                
                print("######################")
                for i in range(0, 101):    #loading a progress bar not accurate of the rendering speed but for decoration
                    pb.value = i * 0.01
                    sleep(0.1)
                    page.update()
                  
                img_viewer.content = img
                page.controls.insert(0, img_viewer)
              
                img.visible = True

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
            img.src = "test_image.png"
            pb.visible = True
            pb.value = 0
            
            for i in range(0, 101):    #loading a progress bar not accurate of the rendering speed but for decoration
                    pb.value = i * 0.01
                    sleep(0.1)
                    page.update()
            
            
            img_viewer.content = img
            
            page.controls.insert(0, img_viewer)


            print((img_viewer.content).src)
            img.visible = True
            
            

            
            pb.visible = False
            pb.value = 0

            page.update()

        
        
        
        
        def validate_name(value):   #validates the name of the render
            if re.fullmatch(r'[A-Za-z0-9#_]+', value):
                return True
            return False
        
        def set_name(e):   #sets the name of the render
            if validate_name(render_name.value):
                name_error_message.visible = False
                render_name.value = render_name.value
                global scene_name
                scene_name = render_name.value
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
        
        def my_renders(e):
            page.controls.clear()
            page.add(
                [ft.Column( 
                    [
                        ft.Text("My Renders", size=30, weight=ft.FontWeight.BOLD),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,  
                )],
                Sign_out_Button,
            )
            page.update()
        
        selected_color = None  # Holds the selected color

        render_name = ft.TextField(label="Render Name",hint_text="e.g., My_Render", width=600, on_change=update_name)
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
            width=300,
        )
        pb = ft.ProgressBar(width=400)
        pb.visible = False
        set = MyButton(text="Set", on_click=set_name)
        object_position = ft.TextField(label="Object Position", hint_text="e.g., (x, y, z)", width=300)
        object_radius = ft.TextField(label="Object Radius", hint_text="e.g., 0.5", width=300)
        color_picker_button = MyButton(text="Pick Color", on_click=pick_color)
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

        Sign_out_Button= Fancy_Button(text="Sign Out", on_click=sign_out,)
        My_Renders_Button= Fancy_Button(text="My Renders", on_click=my_renders,)
        
        if User_Status == True:
            My_Renders_Button.visible = True
        else:
            My_Renders_Button.visible = False
        
        img_viewer = ft.InteractiveViewer(
            min_scale=0.1,
            max_scale=15,
            boundary_margin=ft.margin.all(20),
            content=img,
        )
        
        
        
        def play_next(e):
            audio.release()
            global song_index
    
            audio_file_name = os.path.basename(audio.src)
            song_index = playlist.index(audio_file_name)
            if song_index == len(playlist) - 1:
                song_index = -1
            song_index += 1
            audio_file = os.path.join(radio_folder, playlist[song_index])
            audio.src = audio_file
            print(audio.src)
            page.update()
            audio.play()
            print(f"Playing song: {playlist[song_index]}")
        
        audio.on_seek_complete = play_next
        
        def radio_switch_toggle(e):
            if Radio_switch.value:
                radio.visible = True
                page.update()
                audio.play()
            else:
                radio.visible = False
                audio.pause()
                page.update()
                
        
        
        def resume(e):
            audio.resume()
        def pause(e):
            audio.pause()
        
        Radio_switch = ft.Switch(label="Radio", value=False , on_change= radio_switch_toggle)
        
        radio = ft.Column(
            [   
                ft.Row(
                    [
                    
                    ft.IconButton(
                    icon=ft.icons.SKIP_PREVIOUS_ROUNDED,
                    icon_color="blue400",
                    icon_size=20,
                    tooltip="SKIP BACK",
                    ),
                    
                    
                    ft.IconButton(
                    icon=ft.icons.PLAY_CIRCLE_FILL_OUTLINED,
                    icon_color="blue400",
                    icon_size=20,
                    tooltip="Play",
                    on_click=resume
                    ),
                    
                    ft.IconButton(
                    icon=ft.icons.PAUSE_CIRCLE_FILLED_ROUNDED,
                    icon_color="blue400",
                    icon_size=20,
                    tooltip="Pause",
                    on_click= pause
                    ),

                    ft.IconButton(
                    icon=ft.icons.SKIP_NEXT_ROUNDED,
                    icon_color="blue400",
                    icon_size=20,
                    tooltip="SKIP NEXT",
                    on_click=play_next
                    ),
                    
                    ]
                )
                
                
                           
                           
            ]
                          
                          
        )
        radio.visible = False
        
        radiotile = ft.Row(
            [
                ft.Column(
                    [Radio_switch,
                    radio
                    
                    
                    ]
                ),
                
            ],
            alignment=ft.MainAxisAlignment.START  # Align radiotile to the left
        )

        


        page.add(
            
            pb,
            audio,
            ft.Column(
                [
                    ft.Row(
                        [
                            radiotile,
                            ft.Container(width = 180),
                            ft.Row(
                                
                                
                                [render_name, set],
                                alignment=ft.MainAxisAlignment.CENTER,
                                # render_name and set aligned to the center
                            ),
                            ft.Container(width = 280)
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                          # Ensures proper spacing
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
                            color_picker_button,
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
                    
                    ft.Row(
                        [
                            ft.Column(
                                [
                                    ft.ElevatedButton(text="Radio", on_click=None),
                                ]
                            )
                        ],
                        alignment=ft.MainAxisAlignment.START  # Align radiotile to the left
                    )
                
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
        page.vertical_alignment = ft.MainAxisAlignment.CENTER
        page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    loginpage()

ft.app(main)
