import flet as ft


def main(page: ft.Page):
    
    img_viewer = ft.Container(
        
        content= ft.InteractiveViewer(
            min_scale=0.1,
            max_scale=15,
            boundary_margin=ft.margin.all(20),
            content=ft.Image(
                src="https://picsum.photos/500/500",
            ),
        ),
        border=ft.border.all(2, ft.colors.GREEN_800),
        border_radius=ft.border_radius.all(10),
        )
    
    
    
    
    page.add(img_viewer)
        
    


        

ft.app(main)