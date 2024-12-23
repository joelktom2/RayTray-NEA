import os

current_dir = os.path.dirname(os.path.abspath(__file__))
radio_folder = os.path.join(current_dir, "Radio")

playlist = [f for f in os.listdir(radio_folder) if f.endswith(".mp3")]
print(playlist)

artists_titles = []
