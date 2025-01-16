import flet as ft


def main(page: ft.Page):
    
    def minus_click(e):
        print(e)

    page.add(
        ft.IconButton(ft.icons.REMOVE, on_click=lambda e: minus_click("bingo")),
    )

ft.app(main)