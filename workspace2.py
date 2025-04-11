import flet as ft

def main(page):

    def slider_changed(e):
        t.value = f"Slider changed to {e.control.value}"
        page.update()

    t = ft.Text()
    page.add(
        ft.Text("Slider with 'on_change' event:"),
        ft.Slider(min=20,value = 90, max=150, divisions=130,round = 1, label="{value}",width=500),
    )
ft.app(main)