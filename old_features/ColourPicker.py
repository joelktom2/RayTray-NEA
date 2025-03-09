import flet as ft
from flet_contrib.color_picker import ColorPicker






def pick_color():
    def open_color_picker(e):
        # Add the dialog to the page overlay
        if d not in e.control.page.overlay:
            e.control.page.overlay.append(d)
        d.open = True
        e.control.page.update()

    color_picker = ColorPicker(color="#c8df6f", width=300)
    color_icon = ft.IconButton(icon=ft.icons.BRUSH, on_click=open_color_picker)

    def change_color(e):
        color_icon.icon_color = color_picker.color
        global selected_color
        selected_color = color_picker.color
        d.open = False
        e.control.page.update()

    def close_dialog(e):
        d.open = False
        e.control.page.update()

    d = ft.AlertDialog(
        content=color_picker,
        actions=[
            ft.TextButton("OK", on_click=change_color),
            ft.TextButton("Cancel", on_click=close_dialog),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
        on_dismiss=change_color,
    )

    return color_icon


def my_color_selected(color):
    print(color)

def pick_color2(on_color_selected):
    def open_color_picker(e):
        if d not in e.control.page.overlay:
            e.control.page.overlay.append(d)
        d.open = True
        e.control.page.update()
    
    color_picker = ColorPicker(color="#c8df6f", width=300)
    color_icon = ft.IconButton(icon=ft.icons.BRUSH, on_click=open_color_picker)

    def change_color(e):
        selected_color = color_picker.color
        color_icon.icon_color = selected_color
        d.open = False
        e.control.page.update()
        if on_color_selected:
            on_color_selected(selected_color)
    
    def close_dialog(e):
        d.open = False
        e.control.page.update()
    
    d = ft.AlertDialog(
        content=color_picker,
        actions=[
            ft.TextButton("OK", on_click=change_color),
            ft.TextButton("Cancel", on_click=close_dialog),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
        on_dismiss=close_dialog,
    )
    
    return color_icon







def main(page: ft.Page):
    page.add(
        pick_color2(my_color_selected),
    )

ft.app(main)