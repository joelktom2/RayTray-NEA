from PIL import Image

def convert_ppm_to_png(ppm_file, png_file):
    try:
        # Open the PPM file
        img = Image.open(ppm_file)
        
        # Save as PNG
        img.save(png_file, "PNG")
        print(f"Successfully converted {ppm_file} to {png_file}")
    except Exception as e:
        print(f"Error converting file: {e}")

# Example usage
convert_ppm_to_png("image.ppm", "output.png")
