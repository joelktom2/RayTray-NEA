import flet as ft

def main(page: ft.Page):
    
    page.add(
        ft.TextButton("toggle", on_click=None)
    )

ft.app(main)