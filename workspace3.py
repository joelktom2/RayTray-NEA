import flet as ft

def main(page: ft.Page):
    page.title = "Flet counter example"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    
    def minus_click(text_field,mininum,maximum):
        value = str(int(text_field.value) - 1)

        text_field.value = str(int(text_field.value) - 1)
        
        page.update()

    def plus_click(text_field,mininum,maximum):
        value = str(int(text_field.value) - 1)
        text_field.value = str(int(text_field.value) + 1)
        page.update()

    class IntField(ft.Container):
        def __init__(self, name,min,max):
            super().__init__()
            self.text_field = ft.TextField(
                label=str(name),
                value="0",
                text_align=ft.TextAlign.RIGHT,
                width=80
            )
            self.content = ft.Row(
                [
                    ft.IconButton(
                        icon=ft.icons.REMOVE, 
                        on_click=lambda e: minus_click(self.text_field,min,max)
                    ),
                    self.text_field,
                    ft.IconButton(
                        icon=ft.icons.ADD, 
                        on_click=lambda e: plus_click(self.text_field,min,max)
                    ),
                ]
            )

    joel = IntField("Diffuse",0,1)
    
    def joley(e):
        print(joel.text_field.value)
    page.add(
        ft.Column(
            [
                joel,
                ft.IconButton(icon = ft.icons.ABC, on_click= joley)
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        )
    )

ft.app(main)
