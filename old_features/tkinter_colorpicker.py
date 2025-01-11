from tkinter import Tk, colorchooser


def pick_color(e):   #presents a color picker to the user
            
            root = Tk()
            root.lift()  # Brings the Tkinter root window to the front
            root.attributes("-topmost", True)  # Ensure it's on top
            root.withdraw()  
            color_code = colorchooser.askcolor(title="Choose a color")[1]
            root.destroy()  
            if color_code:
                #nonlocal selected_color
                selected_color = color_code
                #color_picker_button.text = f"Selected: {selected_color}" 
                #color_picker_button.bgcolor = selected_color 
                #page.update()