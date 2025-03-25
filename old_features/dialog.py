import flet as ft


def main(page: ft.Page):
    page.title = "AlertDialog examples"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER



    def handle_close(e):
        page.close(dlg_modal)
        print(f"Name entered: {name.value}")


    name = ft.TextField(label="enter name")
    dlg_modal = ft.AlertDialog(
        modal=True,
        title=ft.Text("Please confirm a name for custom object"),
        content=name,
        actions=[
            ft.TextButton("Ok", on_click=page.close(dlg_modal)),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )

    page.add(
        ft.ElevatedButton("Open modal dialog", on_click=lambda e: page.open(dlg_modal)),
    )


ft.app(main)