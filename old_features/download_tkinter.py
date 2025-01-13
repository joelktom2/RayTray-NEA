import shutil
from tkinter import Tk, filedialog

def download_file(file_path):
    
    # Initialize Tkinter and hide the root window
    root = Tk()
    root.withdraw()
    root.attributes('-topmost', True)  # Bring file dialog to the front

    # Ask user to choose a destination folder
    destination_folder = filedialog.askdirectory(title="Select Destination Folder")
    if not destination_folder:
        print("No destination folder selected. Operation cancelled.")
        return

    # Extract the file name and copy the file to the selected folder
    file_name = file_path.split('/')[-1]
    destination_path = f"{destination_folder}/{file_name}"

    try:
        shutil.copy(file_path, destination_path)
        print(f"File downloaded successfully to: {destination_path}")
    except Exception as e:
        print(f"An error occurred while copying the file: {e}")


