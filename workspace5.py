import win32clipboard
from PIL import Image
import io

def copy_image_to_clipboard(image_path):

    try:
        # Open the image file
        image = Image.open(image_path)

        # Convert the image to BMP format for clipboard compatibility
        output = io.BytesIO()
        image.convert("RGB").save(output, "BMP")
        bmp_data = output.getvalue()[14:]  # Remove the BMP header
        output.close()

        # Open clipboard and set the image data
        win32clipboard.OpenClipboard()
        win32clipboard.EmptyClipboard()
        win32clipboard.SetClipboardData(win32clipboard.CF_DIB, bmp_data)
        win32clipboard.CloseClipboard()

        print("Image successfully copied to the clipboard!")
    except Exception as e:
        print(f"Error copying image to clipboard: {e}")

# Example usage
image_file_path = "download.jpg"  # Replace with your image file path
copy_image_to_clipboard(image_file_path)
