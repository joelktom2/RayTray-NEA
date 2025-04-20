import flet as ft

def main(page: ft.Page):
    def on_result(e: ft.FilePickerResultEvent):
        if e.files:
            file = e.files[0]
            print(f"Selected image: {file.name}")
        else:
            print("No file selected")

    file_picker = ft.FilePicker(
        on_result=on_result
    )

    page.overlay.append(file_picker)

    # This button opens the file picker dialog
    page.add(
        ft.ElevatedButton(
            "Pick an image",
            on_click=lambda _: file_picker.pick_files(
                allow_multiple=False,
                allowed_extensions=["png", "jpg", "jpeg", "bmp", "gif", "webp"]
            )
        )
    )

ft.app(target=main)
