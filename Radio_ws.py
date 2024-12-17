import flet as ft
import os

def main(page: ft.Page):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    radio_folder = os.path.join(current_dir, "Radio")
    global song_index
    song_index = 0
    playlist = [f for f in os.listdir(radio_folder) if f.endswith(".mp3")]
    print(playlist)
    audio_file = os.path.join(radio_folder, playlist[song_index])
    audio = ft.Audio(src=audio_file, autoplay=False)
    
    # Radio tile content
    radiotile = ft.Row(
        [
            ft.Column(
                [
                    ft.ElevatedButton(text="Pause", on_click=lambda e: audio.pause()),
                ]
            )
        ]
    )
    radiotile.visible = False
    
    
    def minimize_radiotile(e):
        radiotile.visible = False
        page.update()  # Update the page
    
    def toggle_radio(e):
        radiotile.visible = True
        
        page.update()
        audio.play()
        
    def play_next(e):
        audio.release()
        global song_index
  
        audio_file_name = os.path.basename(audio.src)
        song_index = playlist.index(audio_file_name)
        if song_index == len(playlist) - 1:
            song_index = -1
        song_index += 1
        audio_file = os.path.join(radio_folder, playlist[song_index])
        audio.src = audio_file
        print(audio.src)
        page.update()
        audio.play()
        print(f"Playing song: {playlist[song_index]}")
        
        
    
    # Audio control
    
    
    minimize_button = ft.ElevatedButton(text="Minimize", on_click=minimize_radiotile)
    start_button = ft.ElevatedButton(text="Radio", on_click=toggle_radio)
    play_next_button = ft.ElevatedButton(text="Next", on_click=play_next)
    
    # Add components to the page
    page.add(
        ft.Text("This is a playlist app."),
        start_button,
        audio,
        ft.Row([radiotile, minimize_button], alignment=ft.MainAxisAlignment.START),
        play_next_button,
        
    )

ft.app(main)
