import flet as ft

def main(page: ft.Page):
    page.title = "Images Example"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 50
    page.update()

    images = ft.Column(expand=1, wrap=False, scroll="always")

    page.add(images)

    for i in range(0, 30):
        images.controls.append(
            ft.Image(
                src="pictures/pic1.jpg",

            )
        )
    page.update()

ft.app(main)
