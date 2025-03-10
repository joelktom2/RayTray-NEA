import flet as ft

def main(page: ft.Page):
    
    hellow = ft.Row([ft.Text(value="Hello, world!"),ft.Text(value="thththjtyj")])
    page.add(hellow)
    hellow.controls[1].value = "ererer"
    page.update()
ft.app(main)

