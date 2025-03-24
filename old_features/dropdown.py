import flet as ft

def main(page: ft.Page):

    icons = [
        {"name": "Smile", "icon_name": ft.icons.SENTIMENT_SATISFIED_OUTLINED},
        {"name": "Cloud", "icon_name": ft.icons.CLOUD_OUTLINED},
        {"name": "Brush", "icon_name": ft.icons.BRUSH_OUTLINED},
        {"name": "Heart", "icon_name": ft.icons.FAVORITE},
    ]

    def get_options():
        options = []
        for icon in icons:
            options.append(
                ft.dropdown.Option(key=icon["name"])
            )
        return options

    dd = ft.Dropdown(
        border=ft.InputBorder.UNDERLINE,
        icon=ft.icons.CLOUD_OUTLINED,
        label="Icon",
        options=get_options(),
    )

    print(dd.options)
    dd.options.append(ft.dropdown.Option(key="New Icon"))
    page.add(dd)


ft.app(main)