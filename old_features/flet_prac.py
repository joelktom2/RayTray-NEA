import flet as ft

def main(page: ft.Page):
    page.title = "Flet counter example"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER




    dd = ft.Dropdown(
            label="Object Type",
            options=[ft.dropdown.Option("Sphere",),
                     ft.dropdown.Option("Floor",),
                     ft.dropdown.Option("Cone"),
                     ft.dropdown.Option("Ellipsoid"),
                     ft.dropdown.Option("Cylinder"),
                     ],
            width=150,
            border_color= ft.colors.GREEN_800,
        )


    txt_number = ft.TextField(value="jeol1", text_align=ft.TextAlign.RIGHT, width=100)
    txt_number2 = ft.TextField(value="joel2", text_align=ft.TextAlign.RIGHT, width=100)
    txt_number3 = ft.TextField(value="jeol3", text_align=ft.TextAlign.RIGHT, width=100)
    rowexam = ft.Row([txt_number, txt_number2, txt_number3], alignment=ft.MainAxisAlignment.CENTER)
    stopper = ft.Text("Stopper")
    


    rowie = ft.Row(
            [
                txt_number,
                dd,
                txt_number2,
                stopper,
                txt_number3,
                rowexam,

            ],
            alignment=ft.MainAxisAlignment.CENTER,
        )
    page.add(
        rowie,
    )
    for x in rowie.controls:
        if x._get_control_name() == "dropdown":
            if x.label == "Object Type":
                print("stopped")
                break
            else:
                print((x._get_control_name()))
        else:
            print(x._get_control_name())
       

ft.app(main)
