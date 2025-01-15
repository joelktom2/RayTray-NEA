import flet
from flet import (
    Column,
    ElevatedButton,
    FilePicker,
    FilePickerResultEvent,
    Page,
    Row,
    Text,
    icons,
)

def main(page: Page):
    

    def directory_picker_result(e: FilePickerResultEvent):
        if e.path:
            print(f"Selected directory: {e.path}")
        else:
            print("No directory selected")
        page.update()

    # Initialize file picker for directory selection
    file_picker = FilePicker(on_result=directory_picker_result)

    # Hide dialog in an overlay
    page.overlay.append(file_picker)

    def select_directory_dialog(e):
        # Open the directory picker dialog to let the user select a directory
        file_picker.get_directory_path(dialog_title="Select Directory")

    page.add(
        ElevatedButton(
            "Select Directory...",
            icon=icons.FOLDER_OPEN,
            on_click=select_directory_dialog,
        ),
        
    )


flet.app(target=main)
