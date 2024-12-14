from time import sleep
import flet as ft
def main(page: ft.Page):
    pb = ft.ProgressBar(width=400)
    pb.value = 0.0
    class MyButton(ft.ElevatedButton):
            def __init__(self, text, on_click):
                super().__init__()
                self.bgcolor = ft.colors.GREEN_100
                self.color = ft.colors.GREEN_800
                self.text = text
                self.on_click = on_click

    def start(e):
        pb.value = 0.0
        for i in range(0, 101):
            pb.value = i * 0.02
            sleep(0.1)
            page.update()
    
    start_button = MyButton("Start", start)
    
    page.add(
        ft.Text("Linear progress indicator", style="headlineSmall"),
        ft.Column([ ft.Text("Doing something..."), pb]),
        start_button,
    )

ft.app(main)