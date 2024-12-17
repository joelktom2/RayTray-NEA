import os
current_dir = os.path.dirname(os.path.abspath(__file__))

radio_folder = os.path.join(current_dir, "Radio")

# Get a list of all MP3 files in the folder
playlist = [f for f in os.listdir(radio_folder) if f.endswith(".mp3")]

print(playlist)