import flet as ft

def main(page: ft.Page):
    
    def button_clicked(e):
        print(f"Dropdown value is:  {object_type.value}")
        

    
    object_type = ft.Dropdown(
            label="Object Type",
            options=[ft.dropdown.Option("Sphere",on_click=lambda e: print(object_type.value)),],
            width=150,
        )
    page.add(object_type)
    b = ft.ElevatedButton(text="Submit", on_click=button_clicked)
    page.add(b)
    
ft.app(main)