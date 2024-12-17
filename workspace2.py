import flet as ft
import os

def main(page: ft.Page):
   
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    radio_folder = os.path.join(current_dir, "Radio")
    
    # Get a list of all MP3 files in the folder
    playlist = [f for f in os.listdir(radio_folder) if f.endswith(".mp3")]

    if not playlist:
        page.add(ft.Text("No MP3 files found in the Radio folder."))
        return

    # Sort playlist (optional, for consistent order)
    #playlist.sort()
    
    # Index to track the currently playing song
    current_index = {"value": 0}  # Use a dictionary to allow mutation in closures

    # Create the Audio component
    
    audio_player = ft.Audio(
        src=, autoplay=False
    )
    page.overlay.append(audio_player)
    def play_next(_):
        """Callback to play the next song in the playlist."""
        if current_index["value"] < len(playlist):
            # Get the next song
            next_song = playlist[current_index["value"]]
            audio_path = os.path.join(radio_folder, next_song)
            
            # Update the audio player's src with the file:// URI
            audio_player.src = f"file://{audio_path}"
            print(f"Now playing: {audio_path}")  # Debugging statement
            page.update()  # Update the page to reflect the change
            audio_player.play()
            current_index["value"] += 1
        else:
            # Reset the playlist (optional)
            current_index["value"] = 0
            page.snack_bar = ft.SnackBar(ft.Text("Playlist finished!"))
            page.snack_bar.open = True
            page.update()

    def start_playlist(_):
        """Start the playlist from the beginning."""
        current_index["value"] = 0
        play_next(None)

    # Attach the callback to play the next song when one ends
    audio_player.on_ended = play_next
    

    # Add UI components
    page.add(
        ft.Text("This is a playlist app."),
        ft.ElevatedButton("Start Playlist", on_click=start_playlist),
    )

ft.app(main)
