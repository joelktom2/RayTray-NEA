import flet as ft
import os
from time import sleep

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
                    ft.ElevatedButton(text="pause", on_click=lambda e: audio.pause()),
                ]
            )
        ]
    )
    radiotile.visible = False
    
    
        #play_next(e=None)
    
    
    
    
    def minimize_radiotile(e):
        radiotile.visible = False
        page.update()  # Update the page
    
    def toggle_radio(e):
        radiotile.visible = True
        
        page.update()
        audio.play()
        
    def play_next(e):
        
        if audio.get_current_position() == 0:
            print("Song ended")
        
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
        
        else:
            print(audio.get_current_position())
            print(audio.get_duration())
            print("Song not ended")
            
        

    def play_next_button(e):
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


        
    
    audio.on_seek_complete = play_next
    
    slider = ft.Slider(value=0.0)
    
    def update_slider(e):
       
        slider.value = audio.get_current_position() / audio.get_duration()
        slider.label = f"{int(slider.value * 100)}%"
        page.update()
        slider.update()


    audio.on_position_changed = update_slider
    
    def manual_slider_update(e):
       
        print("###########################")
        print(slider.value * audio.get_duration())
        print(slider.value)
        print(audio.get_duration())
        audio.seek(int(slider.value * audio.get_duration()))
        page.update()
        slider.update()
        audio.update()
        

    slider.on_change_end = manual_slider_update
        
    # Audio control
    def random(e):
        newpos = int(audio.get_duration() * 0.5)
        print(newpos)
        print(audio.get_duration())
        audio.seek(newpos)
        audio.update()
    
    minimize_button = ft.ElevatedButton(text="Minimize", on_click=minimize_radiotile)
    start_button = ft.ElevatedButton(text="Radio", on_click=toggle_radio)
    play_next_button = ft.ElevatedButton(text="Next", on_click=play_next)
    random_button = ft.ElevatedButton(text="Random", on_click=random)
    
    # Add components to the page
    page.add(
        ft.Text("This is a playlist app."),
        start_button,
        audio,
        ft.Row([radiotile, minimize_button], alignment=ft.MainAxisAlignment.START),
        play_next_button,
        slider,
        random_button,
        
    )

ft.app(main)
